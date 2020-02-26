from loguru import logger

import command
import config
from helpers import is_tmp
import os


def upload_file(file_path):
    buckets = config.APP_GCS_BUCKETS.split(",")
    logger.info(f"Uploading file at path : {file_path}")
    for bucket in buckets:
        upload_command = [
            "/usr/bin/gsutil",
            "cp",
            file_path,
            f"gs://{os.path.join(bucket, os.path.relpath(file_path, config.APP_LANDING_INGEST_DIR))}",
        ]
        if not is_tmp(file_path):
            command.run(upload_command, quiet=True)
        else:
            logger.info("Skipping temp file - {}", {"path": file_path})
