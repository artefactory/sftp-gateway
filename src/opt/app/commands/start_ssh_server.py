from loguru import logger

import command


def start_ssh_server():

    logger.info("Starting SSH")

    start_ssh_command = ["service", "ssh", "start"]

    command.run(start_ssh_command, quiet=True)
