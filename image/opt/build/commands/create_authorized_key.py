import os

import lib.constants as const
import lib.helpers as helpers


def create_authorized_key():

    print "Creating authorized key"

    with open(helpers.get_authorized_key_file(), 'w') as handle:
        with open(const.AUTHORIZED_KEYFILE, 'r') as reader:
            handle.write(reader.read())

    os.chmod(helpers.get_authorized_key_file(), 0644)
    os.chown(helpers.get_authorized_key_file(), const.DEFAULT_UID, const.DEFAULT_GID)
