import config
import log
import os


def create_directories():

    log.info("Creating directories")

    safe_make_dir(config.APP_LANDING_DEV_DIR)
    safe_make_dir(config.APP_LANDING_INGEST_DIR)
    safe_make_dir(config.APP_LANDING_UPLOAD_DIR)
    safe_make_dir(config.APP_LANDING_ERROR_DIR)


def safe_make_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
