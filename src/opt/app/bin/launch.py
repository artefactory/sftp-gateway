"""Summary
"""
from commands.create_directories import create_directories
from commands.populate_environment import populate_environment
from commands.create_user import create_user
from commands.set_landing_permissions import set_landing_permissions
from commands.create_authorized_key import create_authorized_key
from commands.copy_ssh_host_keys import copy_ssh_host_keys
from commands.configure_gcloud import configure_gcloud
from commands.create_sftp_config import create_sftp_config
from commands.move_existing import move_existing
from commands.start_ssh_server import start_ssh_server
from commands.watch_ingest_folder import watch_ingest_folder
import sys

from loguru import logger

if __name__ == "__main__":

    try:
        create_directories()

        populate_environment()
        create_user()
        set_landing_permissions()

        create_authorized_key()
        copy_ssh_host_keys()

        configure_gcloud()
        create_sftp_config()

        move_existing()

        start_ssh_server()

        watch_ingest_folder()

    except Exception as ex:  # pylint: disable=broad-except
        logger.exception(ex)
        sys.exit(1)
