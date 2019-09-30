import commands
import glob
import os

from inotify_simple import INotify, flags
from loguru import logger

import config


def move_existing():
    logger.info("Moving existing files")
    existing_files = glob.glob(os.path.join(config.APP_LANDING_INGEST_DIR, "*"))

    for f in existing_files:
        commands.upload_file(f)


def watch_ingest_folder():
    logger.info("Watching ingestion folder")
    inotify = INotify()
    watched_flags = flags.CREATE | flags.MOVED_TO
    inotify.add_watch(config.APP_LANDING_INGEST_DIR, watched_flags)
    while True:
        events = inotify.read(read_delay=1000)
        for event in events:
            path = os.path.join(config.APP_LANDING_INGEST_DIR, event.name)
            commands.upload_file(path)

