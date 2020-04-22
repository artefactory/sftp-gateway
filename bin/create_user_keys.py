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
import yaml
from src.opt.app import command


def main():
    """Summary
    """
    for user, _ in yaml.load(
            open(f"config/{os.environ['ENV']}.yaml", "r"),
            Loader=yaml.FullLoader)["USERS"].items():
        if not os.path.isdir(f"{os.environ['MK_CREDENTIALS_USERS_DIR']}/{user}"):
            command.run(f"mkdir {os.environ['MK_CREDENTIALS_USERS_DIR']}/{user}")
        if not os.path.isfile(f"{os.environ['MK_CREDENTIALS_USERS_DIR']}/{user}/rsa-key"):
            command.run(
                f'ssh-keygen -N "" -f '
                f'{os.environ["MK_CREDENTIALS_USERS_DIR"]}/{user}/rsa-key'
            )
        if not os.path.isfile(f"{os.environ['MK_CREDENTIALS_USERS_DIR']}/{user}/password"):
            command.run(
                f'openssl rand -out {os.environ["MK_CREDENTIALS_USERS_DIR"]}'
                f'/{user}/password -base64 32'
            )


if __name__ == '__main__':
    main()
