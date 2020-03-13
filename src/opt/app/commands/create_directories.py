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

import config


def create_directories():
    """Summary
    """
    logger.info("Creating directories")

    for user in config.USERS:
        safe_make_dir(f"{user['APP_LANDING_DIR']}")
        safe_make_dir(f"{user['APP_INGEST_DIR']}")


def safe_make_dir(path: str):
    """Summary

    Args:
        path (str): Description
    """
    if not os.path.isdir(path):
        logger.info(f"Directory created : {path}")
        os.makedirs(path)
