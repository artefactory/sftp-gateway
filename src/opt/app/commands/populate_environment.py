import os

from loguru import logger

import config


def populate_environment():

    logger.info("Populating environment file")

    with open(config.ENVIRONMENT_FILE, "w") as handle:

        handle.write("PYTHONPATH=/opt/app/\n")

        for var in os.environ:
            for prefix in config.ENVIRONMENT_VARIABLE_PREFIXES:
                if var.startswith(prefix):

                    kvp = "{}={}\n".format(var, os.environ[var])
                    handle.write(kvp)
                    break
