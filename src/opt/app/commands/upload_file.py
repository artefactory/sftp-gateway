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
import os
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, wait
import csv
from loguru import logger
from google.cloud import storage
from google.oauth2 import service_account
import boto3
import helpers
import config


def get_user_from_path(file_path: str) -> str:
    """Summary
    Args:
        file_path (str): Description
    Returns:
        str: Description
    """
    username = file_path[len(config.APP_LANDING_DIR):].strip('/').split('/')[0]
    return [
        (user, userdata)
        for user, userdata in config.PROJECT_CONFIG["USERS"].items()
        if user == username
    ][0]


class Uploader:

    """Summary
    Attributes:
        google_cloud_storage_clients (dict): Description
    """

    def __init__(self):
        """Summary
        """
        self.google_cloud_storage_clients = {}
        self.aws_s3_clients = {}

    def upload_file(self, file_path: str):
        """Summary
        Args:
            file_path (str): Description
        """
        user, userdata = get_user_from_path(file_path)
        with ThreadPoolExecutor(max_workers=None) as executor:
            futures = []
            futures = self.configure_upload_to_gcs(
                userdata={"name": user, "data": userdata},
                file_path=file_path,
                executor=executor,
                futures=futures
            )
            futures = self.configure_upload_to_s3(
                userdata={"name": user, "data": userdata},
                file_path=file_path,
                executor=executor,
                futures=futures
            )
            wait(futures)
            if config.PROJECT_CONFIG["APP"]["PERSIST_FILES"]:
                os.remove(file_path)
            del futures

    def configure_upload_to_gcs(
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
        for project_id, project_info in userdata["data"].get("GCP_PROJECTS", {}).items():
            if project_id not in self.google_cloud_storage_clients:
                logger.info(f"Configuring GCS client for project {project_id}")
                credentials = service_account.Credentials.from_service_account_file(
                    os.path.join(
                        config.APP_SECRETS_DIR,
                        config.PROJECT_CONFIG["APP"]["NAME"],
                        "users",
                        userdata["name"],
                        "google",
                        f"{project_id}.json"
                    ),
                    scopes=["https://www.googleapis.com/auth/devstorage.read_write"]
                )
                self.google_cloud_storage_clients[project_id] = storage.Client(
                    project=credentials.project_id,
                    credentials=credentials,
                )
            buckets = project_info["BUCKETS"]
            for bucket_name, _ in buckets.items():
                relative_path = os.path.relpath(
                    file_path,
                    os.path.join(config.APP_LANDING_DIR, userdata["name"], 'ingest')
                )
                if not helpers.is_ignored(file_path):
                    logger.info(f"Uploading file to bucket '{bucket_name}' at path : '{file_path}'")
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

    def configure_upload_to_s3(
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
        for account_id, account_info in userdata["data"].get("AWS_ACCOUNTS", {}).items():
            if account_id not in self.aws_s3_clients:
                logger.info(f"Configuring S3 client for account {account_id}")
                with open(os.path.join(
                        config.APP_SECRETS_DIR,
                        config.PROJECT_CONFIG["APP"]["NAME"],
                        "users",
                        userdata["name"],
                        "aws",
                        f"{account_id}.csv"), 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if reader.line_num == 2:
                            access_key_id = row[0]
                            secret_access_key = row[1]
                self.aws_s3_clients[account_id] = boto3.client(
                    "s3",
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key
                )
            for bucket_name, _ in account_info["BUCKETS"].items():
                relative_path = os.path.relpath(
                    file_path,
                    os.path.join(config.APP_LANDING_DIR, userdata["name"], 'ingest')
                )
                if not helpers.is_ignored(file_path):
                    logger.info(f"Uploading file to bucket '{bucket_name}' at path : '{file_path}'")
                    futures += [
                        executor.submit(
                            self.upload_to_s3,
                            account_id,
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

    def upload_to_s3(self, account_id: str, bucket_name: str, file_path: str, relative_path: str):
        """Summary
        Args:
            account_id (str): Description
            bucket_name (str): Description
            file_path (str): Description
            relative_path (str): Description
        """
        with open(file_path, "rb") as file:
            self.aws_s3_clients[account_id].put_object(
                Bucket=bucket_name,
                Body=file,
                Key=relative_path
            )
