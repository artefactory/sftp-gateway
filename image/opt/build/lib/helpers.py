from __future__ import print_function
import os
import sys
from subprocess import check_call, CalledProcessError

import lib.constants as const


def get_landing_directories():
    landing_directories = []
    if 'GCSSFTP_LANDING_DIRECTORIES' in os.environ:
        raw_landing_directories = os.environ['GCSSFTP_LANDING_DIRECTORIES']
        landing_directories = [os.path.join(const.LANDING_DIRECTORY, l.lower()) for l in raw_landing_directories.split(',')]

    return landing_directories


def get_user():
    return os.environ['GCSSFTP_USER']


def get_bucket():
    return os.environ['GCSSFTP_BUCKET']


def get_authorized_key_file():
    return os.path.join(const.AUTHORIZED_KEYS_DIRECTORY, get_user())


def get_template(template):
    template_with_extension = "{}.mustache".format(template)
    return os.path.join(const.TEMPLATE_DIRECTORY, template_with_extension)


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
