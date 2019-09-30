import commands
import sys

from loguru import logger

if __name__ == "__main__":

    try:
        commands.create_directories()

        commands.populate_environment()
        commands.create_user()
        commands.set_landing_permissions()

        commands.create_authorized_key()
        commands.copy_ssh_host_keys()

        commands.configure_gcloud()
        commands.create_sftp_config()

        commands.move_existing()

        commands.start_ssh_server()

        commands.watch_ingest_folder()

    except Exception as ex:
        logger.exception(ex)
        sys.exit(1)
