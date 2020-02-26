"""Summary
"""
import os
import glob
from commands.upload_file import upload_file
from loguru import logger
import config



def move_existing():
    """Summary
    """
    logger.info("Moving existing files")
    existing_files = glob.glob(os.path.join(config.APP_LANDING_INGEST_DIR, "*"))

    for file in existing_files:
        upload_file(file)
