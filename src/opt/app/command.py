import subprocess
import log


def run(command, quiet=False):

    log.debug("Running command {}".format(command))

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    process.wait()

    if not quiet:
        for line in process.stdout:
            log.info(line)

        for line in process.stderr:
            log.error(line)

    log.debug("Command returned exit code {}".format(process.returncode), exit_code=process.returncode)

    if process.returncode != 0:
        raise Exception("Error running command: {}".format(command))

    return process.returncode
