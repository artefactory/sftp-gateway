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
from typing import Dict
import os
import pystache


def render_config(path: str, to_update: Dict):
    """Summary
    Args:
        path (str): Description
        to_update (Dict): Description
    """
    result = {}
    with open(path, "r") as file:
        for line in file.read().split("\n"):
            if len(line.strip()) > 0 and line.strip()[0] != "#":
                os.environ[line.split('=')[0]] = pystache.render(
                    ''.join(line.split('=')[1:]),
                    dict(os.environ)
                ).strip("\'")
                result[line.split('=')[0]] = os.environ[line.split('=')[0]]
    to_update.update(result)
