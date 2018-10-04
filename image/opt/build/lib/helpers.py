from __future__ import print_function
import os
import sys
import base64
from subprocess import check_call, CalledProcessError

import lib.constants as const


def get_landing_directories():
    landing_directories = []
    if 'GCSSFTP_LANDING_DIRECTORIES' in os.environ:
        raw_landing_directories = os.environ['GCSSFTP_LANDING_DIRECTORIES']
        landing_directories = [os.path.join(const.LANDING_DIRECTORY, l.lower()) for l in raw_landing_directories.split(',')]

    return landing_directories


def has_value(key):
    return key in os.environ


def get_ssh_port():
    if has_value('GCSSFTP_SSH_PORT'):
        return os.environ['GCSSFTP_SSH_PORT'].strip()
    return 22


def get_user():
    return os.environ['GCSSFTP_USER'].strip()


def get_bucket():
    return os.environ['GCSSFTP_BUCKET'].strip()


def get_authorized_key():
    return base64.b64decode(os.environ['GCSSFTP_SSH_PUBKEY'])


def gcp_create_service_account_key():
    return base64.b64decode(os.environ['GCSSFTP_SERVICE_ACCOUNT_KEY'])


def get_authorized_key_file():
    return os.path.join(const.AUTHORIZED_KEYS_DIRECTORY, get_user())


def get_template(template):
    template_with_extension = "{}.mustache".format(template)
    return os.path.join(const.TEMPLATE_DIRECTORY, template_with_extension)


def get_project_id():
    return os.environ['GCSSFTP_PROJECT_ID']


def generate_pass():
    return os.urandom(16).encode('hex')


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def command(command):
    try:
        check_call(command)
    except CalledProcessError as ex:
        eprint(ex.output)
        sys.exit(ex.returncode)
