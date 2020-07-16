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
import binascii
import os

from loguru import logger

import command
import config


def create_users():
    """Summary

    Raises:
        Exception: Description
    """
    logger.info("Creating user")

    for user, _ in config.PROJECT_CONFIG["USERS"].items():
        if user in config.FORBIDDEN_USERNAMES:
            raise Exception(f"Username {user} value is invalid")

        create_user_command = (
            f"useradd --no-create-home --no-user-group "
            f"--gid {config.APP_SFTP_GUID} {user}"
        )

        password = open(os.path.join(
            config.APP_SECRETS_DIR,
            config.PROJECT_CONFIG["APP"]["NAME"],
            'users',
            user,
            'password'
        ), 'r').read().split('\n')[0]
        change_password_command = f"yes {password} | passwd {user}"

        change_user_directory_command = (
            f"usermod -d {os.path.join(config.APP_LANDING_DIR, user)} {user}"
        )

        command.run(create_user_command)
        command.run(change_password_command, quiet=True)
        command.run(change_user_directory_command)


def generate_pass():
    """Summary

    Returns:
        str: Description
    """
    return binascii.hexlify(os.urandom(16)).decode()
