import config
import command
import os
import log


def create_user():

    log.info("Creating user")

    if (config.APP_SFTP_USER in config.FORBIDDEN_USERNAMES):
        raise Exception("Username value is invalid")

    create_user_command = ['useradd',
                           '--no-create-home',
                           '--no-user-group',
                           '--uid', str(config.APP_SFTP_UUID),
                           '--gid', str(config.APP_SFTP_GUID),
                           '-p', str(generate_pass()),
                           config.APP_SFTP_USER]

    command.run(create_user_command)


def generate_pass():
    return os.urandom(16).encode('hex')
