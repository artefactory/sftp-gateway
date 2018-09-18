import lib.helpers as helpers
import lib.constants as const


def create_user():
    command = ['useradd',
               '--no-create-home',
               '--no-user-group',
               '--uid', str(const.DEFAULT_UID),
               '--gid', str(const.DEFAULT_GID),
               '-p', str(helpers.generate_pass()),
               helpers.get_user()]

    helpers.command(command)
