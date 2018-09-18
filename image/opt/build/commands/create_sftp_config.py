import pystache

import lib.helpers as helpers
import lib.constants as const


def create_sftp_config():
    renderer = pystache.Renderer()

    context = {
        'authorized_keys_file': helpers.get_authorized_key_file(),
        'user': helpers.get_user(),
        'landing_directory': const.LANDING_DIRECTORY
    }

    config = renderer.render_path(helpers.get_template('sshd_config'), context)

    with open(const.SSHD_CONFIG_FILE, 'w') as h:
        h.write(config)
