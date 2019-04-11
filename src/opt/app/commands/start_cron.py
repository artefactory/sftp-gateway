import command
import log


def start_cron():

    log.info("Starting cron")

    start_cron_command = [
        'service',
        'cron',
        'start'
    ]

    command.run(start_cron_command, quiet=True)
