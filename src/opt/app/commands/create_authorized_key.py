import os

from loguru import logger

import config


def create_authorized_key():

    logger.info("Creating authorized key")

    with open(config.APP_SFTP_AUTHORIZEDKEYS_KEYPATH, 'w') as handle:
        with open(config.APP_SFTP_PUBLICKEY_PATH, 'r') as reader:
            handle.write(reader.read())

    os.chmod(config.APP_SFTP_AUTHORIZEDKEYS_KEYPATH, 0o644)
    os.chown(config.APP_SFTP_AUTHORIZEDKEYS_KEYPATH, int(config.APP_SFTP_UUID), int(config.APP_SFTP_GUID))
