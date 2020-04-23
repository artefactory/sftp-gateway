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
import csv
from loguru import logger
import boto3
from botocore.client import BaseClient
from connectors import BaseUploader
import config


class S3Uploader(BaseUploader):

    """Summary

    Attributes:
        UPLOADER_CONFIG_KEY (str): Description
    """

    UPLOADER_CONFIG_KEY = "AWS_ACCOUNTS"

    def upload(self, _id: str, bucket_name: str, file_path: str, relative_path: str):
        """Summary

        Args:
            _id (str): Description
            bucket_name (str): Description
            file_path (str): Description
            relative_path (str): Description
        """
        with open(file_path, "rb") as file:
            self.clients[_id].put_object(
                Bucket=bucket_name,
                Body=file,
                Key=relative_path
            )

    def get_client(self, _id: str, userdata: Dict) -> BaseClient:
        """Summary

        Args:
            _id (str): Description
            userdata (Dict): Description

        Returns:
            BaseClient: Description
        """
        logger.info(f"Configuring S3 client for account {_id}")
        access_key_id = None
        secret_access_key = None
        with open(os.path.join(
                config.APP_SECRETS_DIR,
                config.PROJECT_CONFIG["APP"]["NAME"],
                "users",
                userdata["name"],
                "aws",
                f"{_id}.csv"), 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if reader.line_num == 2:
                    access_key_id = row[0]
                    secret_access_key = row[1]
        return boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )
