import os

import lib.helpers as helpers
import lib.constants as const


def check_requirements():

    if 'GCSSFTP_USER' not in os.environ:
        raise Exception("Missing GCSSFTP_USER environment variable")

    username = helpers.get_user()

    if not (username and username not in const.FORBIDDEN_USERNAMES):
        raise Exception("GCSSFTP_USER value is invalid")

    if 'GCSSFTP_BUCKET' not in os.environ:
        raise Exception("Missing GCSSFTP_BUCKET environment variable")

    if not helpers.get_bucket():
        raise Exception("GCSSFTP_BUCKET value is invalid")

    for f in [const.SECRET_GCPKEYFILE, const.SECRET_PUBLICKEYFILE]:
        if not os.path.isfile(f):
            raise Exception("{} is not a valid file".format(f))
