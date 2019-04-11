import command
import log


def start_rsyslog():

    log.info("Starting rsyslog")

    start_rsyslog_command = [
        'service',
        'rsyslog',
        'start'
    ]

    command.run(start_rsyslog_command, quiet=True)
