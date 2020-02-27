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
import config
import helpers


def upload_file(file_path: str):
    """Summary

    Args:
        file_path (str): Description
    """
    buckets = config.APP_GCS_BUCKETS.split(",")
    logger.info(f"Uploading file at path : {file_path}")
    for bucket in buckets:
        relative_path = os.path.relpath(file_path, config.APP_LANDING_INGEST_DIR)
        upload_command = [
            "/usr/bin/gsutil",
            "cp",
            file_path,
            f"gs://{os.path.join(bucket, relative_path)}",
        ]
        if not helpers.is_tmp(file_path):
            command.run(upload_command, quiet=True)
        else:
            logger.info("Skipping temp file - {}", {"path": file_path})
