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
import pystache
import config


def create_sftp_config():
    """Summary
    """
    logger.info("Configuring SFTP Config")

    renderer = pystache.Renderer()

    context = {
        "authorized_keys_files": " ".join(
            [
                os.path.join(config.APP_SFTP_AUTHORIZEDKEYS_DIR, user['APP_USERNAME'])
                for user in config.USERS
            ]
        ),
        "users": " ".join([user["APP_USERNAME"] for user in config.USERS]),
        "ssh_port": config.APP_SFTP_PORT
    }

    render_config = renderer.render_path(config.get_template("sshd_config"), context)

    with open(config.SSHD_CONFIG_FILE, "w") as config_file:
        config_file.write(render_config)
