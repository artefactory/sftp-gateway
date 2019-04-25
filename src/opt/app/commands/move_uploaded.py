import log
import shutil
import os
import config
import glob
import fnmatch


_filters = config.APP_LANDING_TEMP_PATTERNS.split(',')


def _move_file_to_upload_directory(path):

    for _f in _filters:
        if fnmatch.fnmatch(path, _f):
            log.info("Skipping file that matches temp pattern: {}".format(_f), path=path)
            return

    destination = os.path.join(config.APP_LANDING_UPLOAD_DIR, os.path.basename(path))
    if os.path.exists(path):
        log.info("Moving {} to {}".format(path, destination))
        shutil.move(path, destination)
    else:
        log.warn("{} doesn't exist, maybe it has been moved?".format(path), path=path)


def move_uploaded(message):
    if 'event' in message:
        if message['event'] in ['sftp_write_file', 'sftp_rename']:
            absolute_path = os.path.join(config.APP_LANDING_DIR, message['path'].lstrip('/'))
            _move_file_to_upload_directory(absolute_path)


def move_existing():
    existing_files = glob.glob(os.path.join(config.APP_LANDING_INGEST_DIR, '*'))

    for f in existing_files:
        _move_file_to_upload_directory(f)
