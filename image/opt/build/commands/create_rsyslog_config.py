import pystache

import lib.helpers as helpers
import lib.constants as const


def create_rsyslog_config():
    renderer = pystache.Renderer()

    context = {
        'landing_directory': const.LANDING_DIRECTORY
    }

    config = renderer.render_path(helpers.get_template('rsyslog'), context)

    with open(const.RSYSLOG_CONFIG_FILE, 'w') as h:
        h.write(config)
