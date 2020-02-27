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
from typing import Dict
import click
from dotenv import dotenv_values
from yaml import dump


# pylint: disable=no-value-for-parameter
@click.command()
@click.option(
    "--env-file", required=True, type=click.File(mode="r"), help="Environment file"
)
@click.option(
    "--secrets-file", required=False, type=click.File(mode="r"), help="Secrets file"
)
def generate(env_file: click.File, secrets_file: click.File):
    """Summary

    Args:
        env_file (click.File): Description
        secrets_file (click.File): Description
    """
    values = dotenv_values(stream=env_file.name)
    yaml_values = {}

    for key, value in values.items():
        _set_value(yaml_values, key, value)

    yaml_values["environment"] = {str(k): str(v) for k, v in values.items()}

    if secrets_file:
        secrets_values = dotenv_values(stream=secrets_file.name)
        yaml_values["secrets"] = {str(k): str(v) for k, v in secrets_values.items()}

    print(dump(yaml_values))


def _set_value(values: Dict[str, str], key: str, value: str):
    """Summary

    Args:
        values (Dict[str, str]): Description
        key (str): Description
        value (str): Description
    """
    parts = list(reversed(key.split("_")))
    stack = values

    while parts:
        part = parts.pop()
        lower_part = str(part.lower())
        if parts:
            stack[lower_part] = stack.get(lower_part, {})
            stack = stack.get(lower_part, {})
        else:
            stack[lower_part] = str(value)


if __name__ == "__main__":
    generate()
