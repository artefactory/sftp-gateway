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
from loguru import logger

import command
import helpers
import config


def upload_file(file_path: str):
    """Summary

    Args:
        file_path (str): Description
    """
    user = get_user_from_path(file_path)
    for project_id, project_info in user["gcs_buckets"].items():
        logger.info(f"Configuring gcloud for project {project_id}")
        auth = [
            "gcloud",
            "auth",
            "activate-service-account",
            "--key-file={}".format(project_info["GCP_SERVICEACCOUNT_KEY_PATH"]),
        ]
        project = ["gcloud", "config", "set", "project", project_id]
        command.run(auth, quiet=True)
        command.run(project, quiet=True)
        buckets = project_info["buckets"]
        logger.info(f"Uploading file at path : {file_path}")
        for bucket in buckets:
            relative_path = os.path.relpath(file_path, user["APP_INGEST_DIR"])
            upload_command = [
                "/usr/bin/gsutil",
                "cp",
                file_path,
                f"gs://{os.path.join(bucket, relative_path)}",
            ]
            if not helpers.is_ignored(file_path):
                command.run(upload_command, quiet=True)
            else:
                logger.info("Skipping temp file - {}", {"path": file_path})


def get_user_from_path(file_path: str):
    username = file_path[len(config.APP_LANDING_BASE):].strip('/').split('/')[0]
    return [user for user in config.USERS if user["APP_USERNAME"] == username][0]
