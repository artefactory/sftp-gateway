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
from commands.create_directories import create_directories
from commands.populate_environment import populate_environment
from commands.create_user import create_user
from commands.set_landing_permissions import set_landing_permissions
from commands.create_authorized_key import create_authorized_key
from commands.copy_ssh_host_keys import copy_ssh_host_keys
from commands.create_sftp_config import create_sftp_config
from commands.move_existing import move_existing
from commands.start_ssh_server import start_ssh_server
from commands.watch_ingest_folder import watch_ingest_folder
import sys

from loguru import logger

if __name__ == "__main__":

    try:
        create_directories()

        populate_environment()
        create_user()
        set_landing_permissions()

        create_authorized_key()
        copy_ssh_host_keys()

        create_sftp_config()

        move_existing()

        start_ssh_server()

        watch_ingest_folder()

    except Exception as ex:  # pylint: disable=broad-except
        logger.exception(ex)
        sys.exit(1)
