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
import shutil
from loguru import logger
import config


def create_authorized_key():
    """Summary
    """
    logger.info("Creating authorized key")

    for user, _ in config.PROJECT_CONFIG["USERS"].items():
        if not os.path.exists(os.path.join(config.APP_LANDING_DIR, user, ".ssh")):
            os.mkdir(os.path.join(config.APP_LANDING_DIR, user, ".ssh"))
        os.chmod(os.path.join(config.APP_LANDING_DIR, user, ".ssh"), 0o700)
        shutil.chown(
            os.path.join(config.APP_LANDING_DIR, user, ".ssh"),
            user,
            int(config.APP_SFTP_GUID)
        )
        with open(os.path.join(
                config.APP_LANDING_DIR,
                user,
                ".ssh",
                "authorized_keys"), 'w') as handle:
            with open(os.path.join(
                    config.APP_SECRETS_DIR,
                    config.PROJECT_CONFIG['APP']['NAME'],
                    "users",
                    user,
                    config.PUBLICKEY_NAME), 'r') as reader:
                handle.write(reader.read())
        os.chmod(os.path.join(config.APP_LANDING_DIR, user, ".ssh", "authorized_keys"), 0o600)
        shutil.chown(
            os.path.join(config.APP_LANDING_DIR, user, ".ssh", "authorized_keys"),
            user,
            int(config.APP_SFTP_GUID)
        )
