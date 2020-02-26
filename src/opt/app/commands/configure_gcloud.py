"""Summary
"""
from loguru import logger

import command
import config


def configure_gcloud():
    """Summary
    """
    logger.info("Configuring gcloud")

    auth = [
        "gcloud",
        "auth",
        "activate-service-account",
        "--key-file={}".format(config.GCP_SERVICEACCOUNT_KEY_PATH),
    ]

    project = ["gcloud", "config", "set", "project", config.GCP_PROJECT_ID]

    command.run(auth, quiet=True)
    command.run(project, quiet=True)
