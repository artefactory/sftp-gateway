import commands
import glob
import os

from inotify_simple import INotify, flags, Event
from loguru import logger

import config


inotify = INotify()
watched_flags = flags.CREATE | flags.MOVED_TO | flags.ISDIR
directories = {}
wds = {}


def move_existing():
    logger.info("Moving existing files")
    existing_files = glob.glob(os.path.join(config.APP_LANDING_INGEST_DIR, "*"))

    for f in existing_files:
        commands.upload_file(f)


def delete_folders_if_empty(dirname):
    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            if not os.listdir(dir_path):  # An empty list is False
                inotify.rm_watch(wds[os.path.join(root, name)])
                del directories[wds[os.path.join(root, name)]]
                del wds[os.path.join(root, name)]
                os.rmdir(os.path.join(root, name))


def get_all_events(events):
    logger.info(f"Initial events: {events}")
    all_events = []
    for event in events:
        is_dir = False
        deleted = False
        for flag in flags.from_mask(event.mask):
            if flag == flag.ISDIR:
                is_dir = True
            if flag == flag.DELETE or flag == flag.IGNORED:
                deleted = True
        if is_dir and not deleted:
            wd = inotify.add_watch(os.path.join(config.APP_LANDING_INGEST_DIR, event.name), watched_flags)
            directories[wd] = os.path.join(config.APP_LANDING_INGEST_DIR, event.name)
            wds[directories[wd]] = wd
            for root, folders, files in os.walk(directories[wd]):
                for folder in folders:
                    wd = inotify.add_watch(os.path.join(root, folder), watched_flags)
                    directories[wd] = os.path.join(root, folder)
                    wds[directories[wd]] = wd
                for file in files:
                    all_events += [Event(wd=wds[root], mask=256, cookie=0, name=file)]
                    logger.info(f"Adding untracked event for file : {root}/{file}")
        elif not deleted:
            all_events += [event]
            logger.info(f"Adding event for file : {directories[event.wd]}/{event.name}")
        else:
            continue
    logger.info(f"All events : {all_events}")
    return all_events


def watch_ingest_folder():
    logger.info("Watching ingestion folder")
    wd = inotify.add_watch(config.APP_LANDING_INGEST_DIR, watched_flags)
    directories[wd] = config.APP_LANDING_INGEST_DIR
    wds[directories[wd]] = wd
    while True:
        events = inotify.read(read_delay=1000)
        all_events = get_all_events(events)
        for event in all_events:
            path = os.path.join(directories[event.wd], event.name)
            commands.upload_file(path)
            os.remove(path)
        delete_folders_if_empty(config.APP_LANDING_INGEST_DIR)
