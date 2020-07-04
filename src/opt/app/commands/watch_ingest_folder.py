# GNU Lesser General Public License v3.0 only
# Copyright (C) 2020 Artefact
# licence-information@artefact.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""Summary
"""
from typing import List

import os
from concurrent.futures import ThreadPoolExecutor
from inotify_simple import INotify, flags, Event
from loguru import logger
from connectors.s3 import S3Uploader
from connectors.gcs import GCSUploader
from connectors import upload_file

import config


class FileWatcher:

    """Summary
    Attributes:
        directories (dict): Description
        inotify (INotify): Description
        users (dict): Description
        watch_descriptors (dict): Description
        watched_flags (int): Description
        uploader (Uploader): Description
    """

    def __init__(self):
        """Summary
        """
        self.inotify = INotify()
        self.watched_flags = flags.CREATE | flags.MOVED_TO | flags.ISDIR
        self.directories = {}
        self.watch_descriptors = {}
        self.users = {}
        self.uploaders = [GCSUploader(), S3Uploader()]
        for user, _ in config.PROJECT_CONFIG["USERS"].items():
            watch_descriptor = self.inotify.add_watch(
                os.path.join(config.APP_LANDING_DIR, user, 'ingest'),
                self.watched_flags
            )
            self.directories[watch_descriptor] = os.path.join(
                config.APP_LANDING_DIR,
                user,
                'ingest'
            )
            self.users[watch_descriptor] = user
            self.watch_descriptors[self.directories[watch_descriptor]] = watch_descriptor
            logger.info("Watching ingestion folder")
        while True:
            events = self.inotify.read(read_delay=1000)
            all_events = self.get_all_events(events)
            with ThreadPoolExecutor(max_workers=None) as executor:
                for event in all_events:
                    executor.submit(
                        upload_file,
                        self.uploaders,
                        os.path.join(self.directories[event.wd], event.name)
                    )

    def get_all_events(self, events: List[Event]) -> List[Event]:
        """Summary
        Args:
            events (List[Event]): Description
        Returns:
            List[Event]: Description
        """
        logger.info(f"Initial events: {events}")
        all_events = []
        for event in events:
            is_dir = False
            deleted = False
            event_user = self.users[event.wd]
            for flag in flags.from_mask(event.mask):
                if flag == flag.ISDIR:
                    is_dir = True
                if flag in (flag.DELETE, flag.IGNORED):
                    deleted = True
            if is_dir and not deleted:
                watch_descriptor = self.inotify.add_watch(
                    os.path.join(config.APP_LANDING_DIR, event_user, "ingest", event.name),
                    self.watched_flags
                )
                self.directories[watch_descriptor] = os.path.join(
                    config.APP_LANDING_DIR, event_user, "ingest", event.name
                )
                self.users[watch_descriptor] = event_user
                self.watch_descriptors[self.directories[watch_descriptor]] = watch_descriptor
                all_events = self.check_subfolders(watch_descriptor, all_events, event_user)
            elif not deleted:
                all_events += [event]
                logger.info(
                    f"Adding event for file : "
                    f"{self.directories[event.wd]}/{event.name}"
                )
            else:
                continue
        logger.info(f"All events : {all_events}")
        return all_events

    def check_subfolders(
            self,
            watch_descriptor: int,
            all_events: List[Event],
            event_user: str) -> List[Event]:
        """Summary
        Args:
            watch_descriptor (int): Description
            all_events (List[Event]): Description
            event_user (str): Description
        Returns:
            List[Event]: Description
        """
        for root, folders, files in os.walk(self.directories[watch_descriptor]):
            for folder in folders:
                watch_descriptor = self.inotify.add_watch(
                    os.path.join(root, folder),
                    self.watched_flags
                )
                self.directories[watch_descriptor] = os.path.join(root, folder)
                self.users[watch_descriptor] = event_user
                self.watch_descriptors[self.directories[watch_descriptor]] = watch_descriptor
            for file in files:
                all_events += [
                    Event(
                        wd=self.watch_descriptors[root],
                        mask=256,
                        cookie=0,
                        name=file)
                ]
                logger.info(f"Adding untracked event for file : {root}/{file}")
        return all_events


def watch_ingest_folder():
    """Summary
    """
    FileWatcher()
