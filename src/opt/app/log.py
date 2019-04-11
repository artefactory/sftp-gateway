import json
import time
import config
from Queue import Queue, Empty
from threading import Thread
import sys
import os
import datetime
import re
import traceback

from parsers import parsers


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


def parse_process(process_str):
    pattern = r'^(.+)\[(\d+)\]:$'
    match = re.match(pattern, process_str)

    if match:
        pname = match.group(1)
        pid = match.group(2)

        if pname not in parsers:
            pname = 'default'
        return pname, int(pid)
    else:
        return "default", -1


def parse_raw(raw_message):
    message = raw_message.strip()
    timestamp, _, process, message = message.split(' ', 3)
    pname, pid = parse_process(process)

    messages = []

    for severity, message, labels in parsers[pname](pid, message):
        labels['pid'] = pid
        payload = {'severity': severity, 'message': message, 'timestamp': timestamp}

        payload.update(labels)
        messages.append(payload)

    return messages


def read_pipe(pipe, message_queue, parser):

    print_for_stackdriver('info', 'Reading pipe {}'.format(pipe))

    worker = Thread(target=_read_pipe, args=(pipe, message_queue, parser))
    worker.setDaemon(True)
    worker.start()


def _read_pipe(pipe, message_queue, parser):
    while True:
        with open(pipe) as handle:
            while True:
                time.sleep(0.1)
                data = handle.readline()

                if len(data) == 0:
                    break

                try:
                    for event in parser(data):
                        message_queue.put((event, None,))
                except Exception as ex:
                    message_queue.put((None, ex,))


def read_log_events():

    message_queue = Queue()

    read_pipe(config.APP_RAW_LOG_PIPE, message_queue, parser=parse_raw)

    keep_on_reading = True

    while keep_on_reading:
        try:
            message_event, _exception = message_queue.get_nowait()
            if not _exception:
                print_for_stackdriver(**message_event)
            else:
                exception(_exception)
                keep_on_reading = False
        except Empty:
            pass
        time.sleep(0.1)
