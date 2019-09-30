import subprocess

from loguru import logger


def run(command, quiet=False):

    logger.debug("Running command {}".format(command))

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    process.wait()

    if not quiet:
        for line in process.stdout:
            logger.info(line)

        for line in process.stderr:
            logger.error(line)

    logger.debug(
        "Command returned exit code - {context}",
        context={"exit_code": process.returncode, "command": command},
    )
    if process.returncode != 0:
        raise Exception("Error running command: {}".format(command))

    return process.returncode
