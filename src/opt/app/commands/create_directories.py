"""Summary
"""
import os

from loguru import logger

import config


def create_directories():
    """Summary
    """
    logger.info("Creating directories")

    safe_make_dir(config.APP_LANDING_DEV_DIR)
    safe_make_dir(config.APP_LANDING_INGEST_DIR)
    safe_make_dir(config.APP_LANDING_UPLOAD_DIR)
    safe_make_dir(config.APP_LANDING_ERROR_DIR)


def safe_make_dir(path: str):
    """Summary

    Args:
        path (str): Description
    """
    if not os.path.isdir(path):
        logger.info(f"Directory created : {path}")
        os.makedirs(path)
