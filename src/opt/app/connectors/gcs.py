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
from typing import Dict
import os
from loguru import logger
from google.cloud import storage
from google.oauth2 import service_account
from connectors import BaseUploader
import config


class GCSUploader(BaseUploader):

    """Summary

    Attributes:
        UPLOADER_CONFIG_KEY (str): Description
    """

    UPLOADER_CONFIG_KEY = "GCP_PROJECTS"

    def upload(self, _id: str, bucket_name: str, file_path: str, relative_path: str):
        """Summary
        Args:
            _id (str): Description
            bucket_name (str): Description
            file_path (str): Description
            relative_path (str): Description
        """
        bucket = self.clients[_id].bucket(bucket_name)
        blob = bucket.blob(relative_path)
        blob.upload_from_filename(file_path)

    def get_client(self, _id: str, userdata: Dict) -> storage.Client:
        logger.info(f"Configuring GCS client for project {_id}")
        credentials = service_account.Credentials.from_service_account_file(
            os.path.join(
                config.APP_SECRETS_DIR,
                config.PROJECT_CONFIG["APP"]["NAME"],
                "users",
                userdata["name"],
                "google",
                f"{_id}.json"
            ),
            scopes=["https://www.googleapis.com/auth/devstorage.read_write"]
        )
        return storage.Client(
            project=credentials.project_id,
            credentials=credentials,
        )
