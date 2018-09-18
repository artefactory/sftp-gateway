import json
import re
import sys
import os

from parsers import parsers

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def print_for_stackdriver(severity, message, timestamp=None, labels={}):

    payload = {
        'message': message,
        'timestamp': timestamp,
        'severity': severity,
        'labels': labels
    }

    print json.dumps(payload)


def parse_process(process_str):
    pattern = r'^(.+)\[(\d+)\]:$'
    match = re.match(pattern, process_str)

    return match.group(1), int(match.group(2))


def parse_timestamp(timestamp_str):
    return timestamp_str.replace('+00:00', 'Z')


def parse(message):
    message = message.strip()
    timestamp, _, process, message = message.split(' ', 3)
    timestamp = parse_timestamp(timestamp)
    pname, pid = parse_process(process)

    for severity, message, labels in parsers[pname](pid, message):
        labels['pid'] = pid
        print_for_stackdriver(severity, message, timestamp, labels)


def read():
    while True:
        print_for_stackdriver("debug", "Opening FIFO")
        with open('/var/run/pipes/consolidated') as handle:
            while True:
                data = handle.readline()
                if len(data) == 0:
                    print_for_stackdriver("debug", "FIFO Closed")
                    break
                parse(data)


if __name__ == '__main__':
    read()
