import commands
import log
import sys


if __name__ == '__main__':

    try:

        commands.populate_environment()
        commands.create_user()
        commands.set_landing_permissions()

        commands.create_authorized_key()
        commands.copy_ssh_host_keys()

        commands.configure_gcloud()
        commands.create_sftp_config()

        commands.create_rsyslog_config()

        commands.start_rsyslog()
        commands.start_ssh_server()
        commands.start_cron()

        log.read_log_events()

    except Exception as ex:
        log.exception(ex)
        sys.exit(1)
