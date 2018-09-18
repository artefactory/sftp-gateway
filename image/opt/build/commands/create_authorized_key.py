import shutil
import os

import lib.constants as const
import lib.helpers as helpers


def create_authorized_key():
    shutil.copy(const.SECRET_PUBLICKEYFILE, helpers.get_authorized_key_file())
    os.chmod(helpers.get_authorized_key_file(), 0644)
    os.chown(helpers.get_authorized_key_file(), const.DEFAULT_UID, const.DEFAULT_GID)
