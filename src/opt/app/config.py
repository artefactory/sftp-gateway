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

Attributes:
    APP_CONFIG_DIR (str): Description
    APP_LANDING_DIR (str): Description
    APP_LANDING_TEMP_PATTERNS (str): Description
    APP_SECRETS_DIR (str): Description
    APP_SFTP_AUTHORIZEDKEYS_DIR (str): Description
    APP_SFTP_GUID (int): Description
    FORBIDDEN_USERNAMES (List): Description
    PROJECT_CONFIG (TYPE): Description
    PUBLICKEY_NAME (str): Description
    SSH_DIR (str): Description
    SSHD_CONFIG_FILE (str): Description
    TEMPLATE_DIRECTORY (TYPE): Description
"""
import os
import yaml


SSH_DIR = "/etc/ssh"
APP_SFTP_AUTHORIZEDKEYS_DIR = "/etc/ssh/authorized-keys"
APP_CONFIG_DIR = "/var/run/config/"
APP_SECRETS_DIR = "/var/run/secrets/"
APP_LANDING_DIR = "/var/landing"
SSHD_CONFIG_FILE = "/etc/ssh/sshd_config"
PUBLICKEY_NAME = "rsa-key.pub"

PROJECT_CONFIG = yaml.load(
    open(f"{os.path.join(APP_CONFIG_DIR, os.environ['APP_NAME'])}.yaml", "r"),
    Loader=yaml.FullLoader
)

FORBIDDEN_USERNAMES = [u.split(':')[0] for u in open('/etc/passwd', 'r').read().split()]

TEMPLATE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'templates')

APP_SFTP_GUID = 9000

APP_LANDING_TEMP_PATTERNS = "*.tmp,*.ssh*,*.cache*"


def get_template(template: str):
    """Summary

    Args:
        template (str): Description

    Returns:
        str: Description
    """
    template_with_extension = "{}.mustache".format(template)
    return os.path.join(TEMPLATE_DIRECTORY, template_with_extension)
