import json
import time

import sys
import os
import datetime

import traceback


sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def info(message, timestamp=None, **kwargs):
    print_for_stackdriver('info', message, timestamp, **kwargs)


def debug(message, timestamp=None, **kwargs):
    print_for_stackdriver('debug', message, timestamp, **kwargs)


def exception(ex, **kwargs):
    print_for_stackdriver('error', 'Error: {}'.format(ex.message), **kwargs)
    print_for_stackdriver('error', 'Traceback: {}'.format(traceback.format_exc()), **kwargs)


def warn(message, timestamp=None, **kwargs):
    print_for_stackdriver('warn', message, timestamp, **kwargs)


def error(message, timestamp=None, **kwargs):
    print_for_stackdriver('error', message, timestamp, **kwargs)


def log_handler(message):
    print_for_stackdriver(**message)


def print_for_stackdriver(severity, message, timestamp=None, **kwargs):

    if timestamp:
        parsed_timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")
        time_seconds = (parsed_timestamp - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    else:
        time_seconds = time.time()

    time_string = "%.9f" % time_seconds

    payload = {
        'message': message.strip(),
        'time': time_string,
        'severity': severity,
        'labels': kwargs
    }

    print json.dumps(payload)
