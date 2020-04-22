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
import shutil
from loguru import logger
import config


def set_landing_permissions():
    """Summary
    """
    logger.info("Setting landing directory permissions")

    for user, _ in config.PROJECT_CONFIG["USERS"].items():
        os.chmod(os.path.join(config.APP_LANDING_DIR, user), 0o755)
        for root, dirs, files in os.walk(f"{os.path.join(config.APP_LANDING_DIR, user)}"):
            for directory in dirs:
                shutil.chown(
                    os.path.join(root, directory),
                    user,
                    int(config.APP_SFTP_GUID)
                )
            for file in files:
                shutil.chown(
                    os.path.join(root, file),
                    user,
                    int(config.APP_SFTP_GUID)
                )
