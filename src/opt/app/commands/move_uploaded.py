import log
import shutil
import os
import config
import glob


def _move_file_to_upload_directory(path):
    destination = os.path.join(config.APP_LANDING_UPLOAD_DIR, os.path.basename(path))
    log.info("Moving {} to {}".format(path, destination))
    shutil.move(path, destination)


def move_uploaded(message):
    if 'event' in message and message['event'] == 'sftp_write_file':
        absolute_path = os.path.join(config.APP_LANDING_DIR, message['path'])
        _move_file_to_upload_directory(absolute_path)


def move_existing():
    existing_files = glob.glob(os.path.join(config.APP_LANDING_INGEST_DIR, '*'))

    for f in existing_files:
        _move_file_to_upload_directory(f)
