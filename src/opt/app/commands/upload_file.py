"""Summary
"""
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
import os
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, wait
from loguru import logger
from google.cloud import storage
from google.oauth2 import service_account
import helpers
import config


def get_user_from_path(file_path: str) -> str:
    """Summary
    Args:
        file_path (str): Description
    Returns:
        str: Description
    """
    username = file_path[len(config.APP_LANDING_BASE):].strip('/').split('/')[0]
    return [user for user in config.USERS if user["APP_USERNAME"] == username][0]


class Uploader:

    """Summary
    Attributes:
        google_cloud_storage_clients (dict): Description
    """

    def __init__(self):
        """Summary
        """
        self.google_cloud_storage_clients = {}

    def upload_file(self, file_path: str):
        """Summary
        Args:
            file_path (str): Description
        """
        user = get_user_from_path(file_path)
        with ThreadPoolExecutor(max_workers=None) as executor:
            futures = []
            futures = self.configure_upload_to_gcs(user, file_path, executor, futures)
            wait(futures)
            if not int(config.APP_PERSIST_FILES):
                os.remove(file_path)
            del futures

    def configure_upload_to_gcs(
            self,
            user: Dict,
            file_path: str,
            executor: ThreadPoolExecutor,
            futures: List
        ) -> List:
        """Summary
        Args:
            user (Dict): Description
            file_path (str): Description
            executor (ThreadPoolExecutor): Description
            futures (List): Description
        Returns:
            List: Description
        """
        for project_id, project_info in user["gcs_buckets"].items():
            if project_id not in self.google_cloud_storage_clients:
                logger.info(f"Configuring GCS client for project {project_id}")
                credentials = service_account.Credentials.from_service_account_file(
                    project_info["GCP_SERVICEACCOUNT_KEY_PATH"],
                    scopes=["https://www.googleapis.com/auth/devstorage.read_write"]
                )
                self.google_cloud_storage_clients[project_id] = storage.Client(
                    project=credentials.project_id,
                    credentials=credentials,
                )
            buckets = project_info["buckets"]
            for bucket_name in buckets:
                relative_path = os.path.relpath(file_path, user["APP_INGEST_DIR"])
                if not helpers.is_ignored(file_path):
                    logger.info(f"Uploading file at path : {file_path}")
                    futures += [
                        executor.submit(
                            self.upload_to_gcs,
                            project_id,
                            bucket_name,
                            file_path,
                            relative_path
                        )
                    ]
                else:
                    logger.info("Skipping temp file - {}", {"path": file_path})
        return futures

    def upload_to_gcs(self, project_id: str, bucket_name: str, file_path: str, relative_path: str):
        """Summary
        Args:
            project_id (str): Description
            bucket_name (str): Description
            file_path (str): Description
            relative_path (str): Description
        """
        bucket = self.google_cloud_storage_clients[project_id].bucket(bucket_name)
        blob = bucket.blob(relative_path)
        blob.upload_from_filename(file_path)
