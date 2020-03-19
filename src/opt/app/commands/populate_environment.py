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
import config


def populate_environment():
    """Summary
    """
    logger.info("Populating environment file")

    with open(config.ENVIRONMENT_FILE, "w") as handle:

        handle.write("PYTHONPATH=/opt/app/\n")

        for var in os.environ:
            for prefix in config.ENVIRONMENT_VARIABLE_PREFIXES:
                if var.startswith(prefix):
                    kvp = "{}={}\n".format(var, os.environ[var])
                    handle.write(kvp)
                    break
