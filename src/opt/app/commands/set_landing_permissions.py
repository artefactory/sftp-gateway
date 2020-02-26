"""Summary
"""
import os

from loguru import logger

import config


def set_landing_permissions():
    """Summary
    """
    logger.info("Setting landing directory permissions")

    for root, dirs, files in os.walk(config.APP_LANDING_DIR):

        for directory in dirs:
            chown(os.path.join(root, directory))
        for file in files:
            chown(os.path.join(root, file))


def chown(path: str):
    """Summary

    Args:
        p (str): Description
    """
    os.chown(path, int(config.APP_SFTP_UUID), int(config.APP_SFTP_GUID))
