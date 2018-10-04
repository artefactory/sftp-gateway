import os

import lib.constants as const
import lib.helpers as helpers


def create_landing():

    print "Creating landing"

    for directory in helpers.get_landing_directories():
        os.mkdir(directory)
        os.chown(directory, const.DEFAULT_UID, const.DEFAULT_GID)
