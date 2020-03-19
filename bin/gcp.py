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
from bin import render_config
import json
from googleapiclient import discovery, errors
import click
from base64 import b64decode


config = {}
render_config(f"config/{os.environ['ENV']}", config)


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
def create_gcp_service_accounts(ctx):
    iam_service = discovery.build('iam', 'v1')
    resource_manager_service = discovery.build('cloudresourcemanager', 'v1')
    for user in os.listdir("env/users"):
        userdata = json.loads(config[f"SFTP_USER_{user}"])
        if "gcs_buckets" in userdata:
            for project_id, user_project_data in userdata["gcs_buckets"].items():
                key_path = f"credentials/{os.environ['ENV']}/users/{user_project_data['GCP_SERVICEACCOUNT_KEY_NAME']}"
                if not os.path.exists(key_path):
                    service_account = None
                    try:
                        service_account = get_service_account(project_id, user_project_data["GCP_SERVICEACCOUNT_IAM"], iam_service)
                        print(f'Service account already exists for user : {user_project_data["GCP_SERVICEACCOUNT_IAM"]} !')
                    except errors.HttpError:
                        print(f'Creating service account for user : {user_project_data["GCP_SERVICEACCOUNT_IAM"]} !')
                        service_account = create_service_account(
                            project_id,
                            user_project_data["GCP_SERVICEACCOUNT_NAME"],
                            user_project_data["GCP_SERVICEACCOUNT_NAME"],
                            iam_service
                        )
                        print(f"Created service account : {service_account['email']}")
                        add_service_account_policy(project_id, service_account, resource_manager_service)
                    print(f'Creating service account key for user : {user_project_data["GCP_SERVICEACCOUNT_IAM"]} !')
                    created_key = create_service_account_key(service_account, iam_service)
                    key_directory = os.path.join(*key_path.split("/")[:-1])
                    if not os.path.exists(key_directory):
                        os.mkdir(key_directory)
                    with open(key_path, 'wb') as f:
                        f.write(b64decode(created_key["privateKeyData"]))
                    print(f'Done creating key at path {key_path}')
                else:
                    print(f"Key already found for project {project_id} and user {user}")


def get_service_account(project_id, service_account_email, iam_service):
    return iam_service.projects().serviceAccounts().get(name=f"projects/{project_id}/serviceAccounts/{service_account_email}").execute()


def add_service_account_policy(project_id, service_account, resource_manager_service):
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


def get_project_policies(project_id, resource_manager_service):
    return resource_manager_service.projects().getIamPolicy(
        resource=project_id, body={"options": {"requestedPolicyVersion": 3}}
    ).execute()


def create_service_account(project_id, name, display_name, iam_service):
    service_account = iam_service.projects().serviceAccounts().create(
        name='projects/' + project_id,
        body={
            'accountId': name,
            'serviceAccount': {
                'displayName': display_name
            }
        }).execute()
    return service_account


def create_service_account_key(service_account, iam_service):
    return iam_service.projects().serviceAccounts().keys().create(
        name=service_account["name"],
        body={
            "privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE",
            "keyAlgorithm": "KEY_ALG_RSA_2048"
        }
    ).execute()


if __name__ == '__main__':
    cli()
