import glob
import os
import shutil
import stat

from loguru import logger

import config


def copy_ssh_host_keys():

    logger.info("Copying SSH Host keys")

    path = os.path.join(config.APP_SECRETS_DIR, "ssh_host*")

    for host_key in glob.glob(path):
        destination = os.path.join(config.SSH_DIR, os.path.basename(host_key))

        logger.info("Copying {} to {}".format(host_key, destination))
        shutil.copy(host_key, destination)

        os.chmod(destination, stat.S_IREAD)
