import pystache
import config
import log


def create_rsyslog_config():

    log.info("Configuring rsyslog")

    generate_rsyslog_main_config()
    generate_rsyslog_default_config()


def generate_rsyslog_default_config():

    renderer = pystache.Renderer()

    context = {
        'raw_syslog_pipe': config.APP_RAW_LOG_PIPE,
        'raw_syslog_facility': config.APP_RAW_LOG_FACILITY
    }

    render_config = renderer.render_path(config.get_template('50-default'), context)

    with open(config.RSYSLOG_DEFAULT_CONFIG_FILE, 'w') as h:
        h.write(render_config)


def generate_rsyslog_main_config():

    renderer = pystache.Renderer()

    context = {
        'log_device': config.APP_LANDING_LOG_DEVICE
    }

    render_config = renderer.render_path(config.get_template('rsyslog'), context)

    with open(config.RSYSLOG_CONFIG_FILE, 'w') as h:
        h.write(render_config)
