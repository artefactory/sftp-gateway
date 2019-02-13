from __future__ import print_function
import os
import sys
from subprocess import check_call, CalledProcessError

import lib.constants as const


def has_value(key):
    return key in os.environ


def get_user():
    return os.environ['SFTP_USER'].strip()


def get_bucket():
    return os.environ['GCS_BUCKET'].strip()


def get_authorized_key_file():
    return os.path.join(const.AUTHORIZED_KEYS_DIRECTORY, get_user())


def get_template(template):
    template_with_extension = "{}.mustache".format(template)
    return os.path.join(const.TEMPLATE_DIRECTORY, template_with_extension)


def get_project_id():
    return os.environ['PROJECT_ID']


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
