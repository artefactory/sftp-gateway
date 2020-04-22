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
import glob
import os
import shutil
import stat

from loguru import logger
import config


def copy_ssh_host_keys():
    """Summary
    """
    logger.info("Copying SSH Host keys")

    path = os.path.join(
        config.APP_SECRETS_DIR,
        config.PROJECT_CONFIG['APP']['NAME'],
        "internal",
        "ssh-host-*"
    )

    for host_key in glob.glob(path):
        destination = os.path.join(config.SSH_DIR, os.path.basename(host_key))

        logger.info("Copying {} to {}".format(host_key, destination))
        shutil.copy(host_key, destination)

        os.chmod(destination, stat.S_IREAD)
