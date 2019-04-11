import os
import config
import log


def set_landing_permissions():

    log.info("Setting landing directory permissions")

    for root, dirs, files in os.walk(config.APP_LANDING_DIR):

        for d in dirs:
            chown(os.path.join(root, d))
        for f in files:
            chown(os.path.join(root, f))


def chown(p):
    os.chown(p, int(config.APP_SFTP_UUID), int(config.APP_SFTP_GUID))
