"""Summary

Deleted Attributes:
    data (dict): Description
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
import os
import json
from typing import Dict
from bin import render_config


def generate_gcs_config():
    """Summary
    """
    data = {}
    render_config(f"env/{os.environ['ENV']}", data)
    render_config(f"env/common", data)
    for user in os.listdir("env/users"):
        data[user] = {}
        render_config(f"env/users/{user}", data[user])
        render_config(f"env/config/landing", data[user])
        data[user]["SFTP_UUID"] = int(os.environ["APP_SFTP_UUID"]) + 1
        data["APP_SFTP_UUID"] = int(os.environ["APP_SFTP_UUID"]) + 1
        data = generate_gcs_config_for_user(data, user)
        os.environ["APP_SFTP_UUID"] = f'{data[user]["SFTP_UUID"]}'
    with open(f"config/{os.environ['ENV']}", "w") as file:
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                file.write(f'SFTP_USER_{key}=\'{json.dumps(value)}\'\n')
            else:
                file.write(f'{key}={value}\n')


def generate_gcs_config_for_user(data: Dict, username: str) -> Dict:
    """Summary
    Args:
        data (Dict): Description
        username (str): Description
    Returns:
        Dict: Description
    """
    if "GCP_BUCKET_PROJECT_IDS" in os.environ and "APP_GCS_BUCKETS" in os.environ:
        data[username]["gcs_buckets"] = {}
        for gcs_bucket_name, gcs_bucket_project_id in zip(
                os.environ.get("APP_GCS_BUCKETS", "").split(','),
                os.environ.get("GCP_BUCKET_PROJECT_IDS", "").split(',')
            ):
            if gcs_bucket_project_id not in data[username]["gcs_buckets"]:
                data[username]["gcs_buckets"][gcs_bucket_project_id] = {}
            data[username]["gcs_buckets"][gcs_bucket_project_id]["buckets"] = (
                data[username]["gcs_buckets"][gcs_bucket_project_id].get("buckets", []) +
                [gcs_bucket_name]
            )
            os.environ["GCP_BUCKET_PROJECT_ID"] = gcs_bucket_project_id
            render_config(f"env/config/gcs", data[username]["gcs_buckets"][gcs_bucket_project_id])
        del os.environ["APP_GCS_BUCKETS"]
        del os.environ["GCP_BUCKET_PROJECT_IDS"]
        data[username].pop("APP_GCS_BUCKETS")
        data[username].pop("GCP_BUCKET_PROJECT_IDS")
    for key in data[username].keys():
        if key not in ["SFTP_UUID", "gcs_buckets"]:
            del os.environ[key]
        if "GCP_BUCKET_PROJECT_ID" in os.environ:
            del os.environ["GCP_BUCKET_PROJECT_ID"]
    return data


if __name__ == '__main__':
    generate_gcs_config()
