"""Summary
"""
import os
from loguru import logger

import command
import config
import helpers


def upload_file(file_path: str):
    """Summary

    Args:
        file_path (str): Description
    """
    buckets = config.APP_GCS_BUCKETS.split(",")
    logger.info(f"Uploading file at path : {file_path}")
    for bucket in buckets:
        relative_path = os.path.relpath(file_path, config.APP_LANDING_INGEST_DIR)
        upload_command = [
            "/usr/bin/gsutil",
            "cp",
            file_path,
            f"gs://{os.path.join(bucket, relative_path)}",
        ]
        if not helpers.is_tmp(file_path):
            command.run(upload_command, quiet=True)
        else:
            logger.info("Skipping temp file - {}", {"path": file_path})
