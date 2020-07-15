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
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, wait
import os
from loguru import logger
import time
import config
import helpers


def wait_for_file_readiness(file_path: str):
    logger.debug(f"Trying to fetch file {file_path}...")
    size = 0
    while os.path.getsize(file_path) != size:
        size = os.path.getsize(file_path)
        time.sleep(3)
    return True


def upload_file(uploaders: List, file_path: str):
    """Summary
    Args:
        uploaders (List): Description
        file_path (str): Description
    """
    user, userdata = helpers.get_user_from_path(file_path)
    wait_for_file_readiness(file_path)
    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = []
        for uploader in uploaders:
            futures = uploader.configure_upload(
                userdata={"name": user, "data": userdata},
                file_path=file_path,
                executor=executor,
                futures=futures
            )
        wait(futures)
        if not config.PROJECT_CONFIG["APP"]["PERSIST_FILES"]:
            os.remove(file_path)
        del futures


class BaseUploader:

    """Summary

    Attributes:
        clients (dict): Description
    """

    def __init__(self):
        """Summary
        """
        self.clients = {}

    def configure_upload(
            self,
            userdata: Dict,
            file_path: str,
            executor: ThreadPoolExecutor,
            futures: List) -> List:
        """Summary

        Args:
            userdata (Dict): Description
            file_path (str): Description
            executor (ThreadPoolExecutor): Description
            futures (List): Description

        Returns:
            List: Description
        """
        for _id, info in userdata["data"].get(self.UPLOADER_CONFIG_KEY, {}).items():
            if _id not in self.clients:
                self.clients[_id] = self.get_client(_id, userdata)
            buckets = info["BUCKETS"]
            for bucket_name, _ in buckets.items():
                relative_path = os.path.relpath(
                    file_path,
                    os.path.join(config.APP_LANDING_DIR, userdata["name"], 'ingest')
                )
                if not helpers.is_ignored(file_path):
                    logger.info(f"Uploading file to bucket '{bucket_name}' at path : '{file_path}'")
                    futures += [
                        executor.submit(
                            self.upload,
                            _id,
                            bucket_name,
                            file_path,
                            relative_path
                        )
                    ]
                else:
                    logger.info("Skipping temp file - {}", {"path": file_path})
        return futures

    def upload(self, _id: str, bucket_name: str, file_path: str, relative_path: str):
        """Summary

        Args:
            _id (str): Description
            bucket_name (str): Description
            file_path (str): Description
            relative_path (str): Description

        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError()

    def get_client(self, _id: str, userdata: Dict):
        """Summary

        Args:
            _id (str): Description
            userdata (Dict): Description

        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError()
