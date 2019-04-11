import command
import log


def start_ssh_server():

    log.info("Starting SSH")

    start_ssh_command = [
        'service',
        'ssh',
        'start'
    ]

    command.run(start_ssh_command, quiet=True)
