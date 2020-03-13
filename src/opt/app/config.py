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
    APP_SFTP_AUTHORIZEDKEYS_KEYPATH (str): Description
    ENVIRONMENT_FILE (str): Description
    ENVIRONMENT_VARIABLE_PREFIXES (list): Description
    FORBIDDEN_USERNAMES (list): Description
    SSH_DIR (str): Description
    SSHD_CONFIG_FILE (str): Description
    TEMPLATE_DIRECTORY (str): Description
"""
import os
import json

for variable, value in os.environ.items():
    locals()[variable.strip()] = value.strip()


FORBIDDEN_USERNAMES = [u.split(':')[0] for u in open('/etc/passwd', 'r').read().split()]

INPUT_CONFIG = locals().copy()

USERS = []
for key, value in INPUT_CONFIG.items():
    if key[:len('SFTP_USER_')] == "SFTP_USER_":
        USERS += [json.loads(INPUT_CONFIG[key][1:-1])]


TEMPLATE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'templates')

SSH_DIR = "/etc/ssh"
SSHD_CONFIG_FILE = "/etc/ssh/sshd_config"

ENVIRONMENT_FILE = "/etc/environment"
ENVIRONMENT_VARIABLE_PREFIXES = ['APP_', 'GCP_']


def get_template(template: str):
    """Summary

    Args:
        template (str): Description

    Returns:
        str: Description
    """
    template_with_extension = "{}.mustache".format(template)
    return os.path.join(TEMPLATE_DIRECTORY, template_with_extension)
