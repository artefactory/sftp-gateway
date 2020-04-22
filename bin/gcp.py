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
    CONFIG (dict): Description
"""
import os
from base64 import b64decode
from typing import Dict
import click
from googleapiclient import discovery, errors
import yaml


CONFIG = yaml.load(open(f"config/{os.environ['ENV']}.yaml", "r"), Loader=yaml.FullLoader)


@click.group()
def cli():
    """Summary
    """


@cli.command()
def create_gcp_service_accounts():
    """Summary
    """
    ask_key_creation = input("Do you want to create user access keys ? (y/n): ")
    if ask_key_creation in ["y", "Y", "yes", "Yes"]:
        for user, userdata in CONFIG["USERS"].items():
            if "GCP_PROJECTS" in userdata:
                for project_id, _ in userdata["GCP_PROJECTS"].items():
                    set_user_service_account(project_id, user)
    else:
        print("Did not create any user service account...")


def set_user_service_account(project_id: str, user: str):
    """Summary
    Args:
        project_id (str): Description
        user (str): Description
    """
    key_path = (
        f"credentials/{os.environ['ENV']}/users/"
        f"{user}/google/{project_id}.json"
    )
    if not os.path.exists(key_path):
        service_account = None
        iam_service = discovery.build('iam', 'v1')
        resource_manager_service = discovery.build('cloudresourcemanager', 'v1')
        try:
            service_account = get_service_account(
                project_id,
                f"{user}-sftp@{project_id}.iam.gserviceaccount.com",
                iam_service
            )
            print(
                f'Service account already exists for user : '
                f"{user}-sftp@{project_id}.iam.gserviceaccount.com !"
            )
        except errors.HttpError:
            print(
                f'Creating service account for user : '
                f"{user}-sftp@{project_id}.iam.gserviceaccount.com !"
            )
            service_account = create_service_account(
                project_id,
                f"{user}-sftp",
                f"{user}-sftp",
                iam_service
            )
            print(f"Created service account : {service_account['email']}")
            add_service_account_policy(
                project_id,
                service_account,
                resource_manager_service
            )
        print(
            f'Creating service account key for user : '
            f'{user}-sftp !'
        )
        created_key = create_service_account_key(service_account, iam_service)
        key_directory = os.path.join(*key_path.split("/")[:-1])
        if not os.path.exists(key_directory):
            os.mkdir(key_directory)
        with open(key_path, 'wb') as file:
            file.write(b64decode(created_key["privateKeyData"]))
        print(f'Done creating key at path {key_path}')
    else:
        print(f"Key already found for project {project_id} and user {user}")


def get_service_account(
        project_id: str,
        service_account_email: str,
        iam_service: discovery.Resource) -> Dict:
    """Summary
    Args:
        project_id (str): Description
        service_account_email (str): Description
        iam_service (discovery.Resource): Description
    Returns:
        Dict: Description
    """
    return iam_service.projects().serviceAccounts().get(
        name=f"projects/{project_id}/serviceAccounts/{service_account_email}"
    ).execute()


def add_service_account_policy(
        project_id: str,
        service_account: Dict,
        resource_manager_service: discovery.Resource) -> Dict:
    """Summary
    Args:
        project_id (str): Description
        service_account (Dict): Description
        resource_manager_service (discovery.Resource): Description
    Returns:
        Dict: Description
    """
    existing_policies = get_project_policies(project_id, resource_manager_service)
    new_policies = existing_policies
    new_policies["bindings"] += [{
        "role": f"roles/storage.objectAdmin",
        "members": [
            f'serviceAccount:{service_account["email"]}'
        ]
    }]
    return resource_manager_service.projects().setIamPolicy(
        resource=f'{project_id}',
        body={"policy": new_policies}
    ).execute()


def get_project_policies(
        project_id: str,
        resource_manager_service: discovery.Resource) -> Dict:
    """Summary
    Args:
        project_id (str): Description
        resource_manager_service (discovery.Resource): Description
    Returns:
        Dict: Description
    """
    return resource_manager_service.projects().getIamPolicy(
        resource=project_id, body={"options": {"requestedPolicyVersion": 3}}
    ).execute()


def create_service_account(
        project_id: str,
        name: str,
        display_name: str,
        iam_service: discovery.Resource) -> Dict:
    """Summary
    Args:
        project_id (str): Description
        name (str): Description
        display_name (str): Description
        iam_service (discovery.Resource): Description
    Returns:
        Dict: Description
    """
    return iam_service.projects().serviceAccounts().create(
        name='projects/' + project_id,
        body={
            'accountId': name,
            'serviceAccount': {
                'displayName': display_name
            }
        }
    ).execute()


def create_service_account_key(
        service_account: Dict,
        iam_service: discovery.Resource) -> Dict:
    """Summary
    Args:
        service_account (Dict): Description
        iam_service (discovery.Resource): Description
    Returns:
        Dict: Description
    """
    return iam_service.projects().serviceAccounts().keys().create(
        name=service_account["name"],
        body={
            "privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE",
            "keyAlgorithm": "KEY_ALG_RSA_2048"
        }
    ).execute()


if __name__ == '__main__':
    cli()
