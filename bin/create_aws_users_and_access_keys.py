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
import csv
from datetime import date
import json
import boto3
from botocore.client import BaseClient
import yaml
from src.opt.app import command


CONFIG = None
with open(f"config/{os.environ['ENV']}.yaml", "r", encoding="utf8") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)


def create_aws_access_keys():
    """Summary
    """
    account_ids = []
    iam_clients = {}
    policy_document = {
        "Version": date.today().strftime("%Y-%m-%d"),
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:*"],
                "Resource": "*"
            }
        ]
    }
    for user, userdata in CONFIG["USERS"].items():
        if "AWS_ACCOUNTS" in userdata:
            for account_id, _ in userdata["AWS_ACCOUNTS"].items():
                if account_id not in account_ids:
                    account_ids += [account_id]
    ask_key_creation = input("Do you want to create user access keys ? (y/n): ")
    if ask_key_creation in ["y", "Y", "yes", "Yes"]:
        for account_id in account_ids:
            print(
                f"Please, setup your admin access keys for Account ID"
                f"(no admin access keys are used online) : {account_id}"
            )
            aws_access_key_id = input("AWS Access Key ID :")
            aws_secret_access_key = input("AWS Secret Access Key :")
            command.run(
                f"aws configure set aws_access_key_id "
                f"{aws_access_key_id} --profile {account_id}"
            )
            command.run(
                f"aws configure set aws_secret_access_key "
                f"{aws_secret_access_key} --profile {account_id}"
            )
            boto3.setup_default_session(profile_name=account_id)
            iam_clients[account_id] = boto3.client('iam')
            iam_clients[account_id].create_policy(
                Path=f"arn:aws:iam::{account_id}:policy/sftp-users",
                PolicyName="sftp-users",
                PolicyDocument=json.dumps(policy_document, indent=4),
                Description="Policy for Nautilus SFTP user"
            )
        for user, userdata in CONFIG["USERS"].items():
            if "AWS_ACCOUNTS" in userdata:
                for account_id, _ in userdata["AWS_ACCOUNTS"].items():
                    set_user(iam_clients[account_id], account_id, user)
    else:
        print("Did not create user access keys...")


def set_user(iam: BaseClient, account_id: str, user: str):
    """Summary
    Args:
        account_id (str): Description
        user (str): Description
    """
    key_path = (
        f"credentials/{os.environ['ENV']}/users/"
        f"{user}/aws/{account_id}.csv"
    )
    if not os.path.exists(key_path):
        try:
            iam.get_user(f'{user}-sftp')
            print(
                f"User {user}-sftp already exists !"
            )
        except iam.meta.client.exceptions.NoSuchEntityException:
            print(
                f'Creating user : '
                f"{user}-sftp"
            )
            iam.create_user(
                Path=f'arn:aws:iam::{account_id}:user/{user}-sftp',
                UserName=f'{user}-sftp',
                PermissionsBoundary=f"arn:aws:iam::{account_id}:policy/sftp-users"
            )
            print(f"Created user : {user}")
        print(
            f'Creating access key for user : '
            f'{user}-sftp !'
        )
        created_key = iam.create_access_key(UserName=f"{user}-sftp")
        key_directory = os.path.join(*key_path.split("/")[:-1])
        if not os.path.exists(key_directory):
            os.mkdir(key_directory)
        with open(key_path, 'w', encoding="utf8") as file:
            writer = csv.writer(file)
            for row in [
                    ["Access key ID", "Secret access key"],
                    [
                        created_key['AccessKey']['AccessKeyId'],
                        created_key['AccessKey']['SecretAccessKey']
                    ]]:
                writer.writerow(row)
        print(f'Done creating key at path {key_path}')
    else:
        print(f"Key already found for project {account_id} and user {user}")


if __name__ == '__main__':
    create_aws_access_keys()
