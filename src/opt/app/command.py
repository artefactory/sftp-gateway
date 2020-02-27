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
import subprocess

from loguru import logger


def run(command: str, quiet: bool = False):
    """Summary

    Args:
        command (str): Description
        quiet (bool, optional): Description

    Returns:
        int: Description

    Raises:
        Exception: Description
    """
    logger.debug("Running command {}".format(command))

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    process.wait()

    if not quiet:
        for line in process.stdout:
            logger.info(line)

        for line in process.stderr:
            logger.error(line)

    logger.debug(
        "Command returned exit code - {context}",
        context={"exit_code": process.returncode, "command": command},
    )
    if process.returncode != 0:
        raise Exception("Error running command: {}".format(command))

    return process.returncode
