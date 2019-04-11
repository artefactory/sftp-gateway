import os
import shutil
import glob
import config
import log
import stat


def copy_ssh_host_keys():

    log.info("Copying SSH Host keys")

    path = os.path.join(config.APP_SECRETS_DIR, 'ssh_host*')

    for host_key in glob.glob(path):
        destination = os.path.join(config.SSH_DIR, os.path.basename(host_key))

        log.info("Copying {} to {}".format(host_key, destination))
        shutil.copy(host_key, destination)

        os.chmod(destination, stat.S_IREAD)
