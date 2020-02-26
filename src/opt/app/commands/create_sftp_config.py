"""Summary
"""
from loguru import logger
import pystache
import config


def create_sftp_config():
    """Summary
    """
    logger.info("Configuring SFTP Config")

    renderer = pystache.Renderer()

    context = {
        "authorized_keys_file": config.APP_SFTP_AUTHORIZEDKEYS_KEYPATH,
        "user": config.APP_SFTP_USER,
        "landing_directory": config.APP_LANDING_DIR,
        "ssh_port": config.APP_SFTP_PORT,
        "syslog_facility": config.SYSLOG_FACILITY
    }

    render_config = renderer.render_path(config.get_template("sshd_config"), context)

    with open(config.SSHD_CONFIG_FILE, "w") as config_file:
        config_file.write(render_config)
