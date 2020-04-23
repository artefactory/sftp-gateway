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
import glob
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
from connectors.gcs import GCSUploader
from connectors.s3 import S3Uploader
from connectors import upload_file
import config


def move_existing():
    """Summary
    """
    logger.info("Moving existing files")
    uploaders = [S3Uploader(), GCSUploader()]
    with ThreadPoolExecutor(max_workers=None) as executor:
        for user, _ in config.PROJECT_CONFIG["USERS"].items():
            existing_files = glob.glob(os.path.join(config.APP_LANDING_DIR, user, 'ingest', "*"))
            for file in existing_files:
                executor.submit(
                    upload_file,
                    uploaders,
                    file
                )
