import commands


if __name__ == '__main__':
    commands.check_requirements()
    commands.create_user()
    commands.create_authorized_key()
    commands.configure_gcloud()
    commands.create_sftp_config()
    commands.create_rsyslog_config()
