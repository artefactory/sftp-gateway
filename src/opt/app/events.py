import time
import config
from Queue import Queue, Empty
from threading import Thread
import re
import log
from parsers import parsers


_event_handlers = {}


def register_event_handler(name, handler):
    global _event_handlers
    _event_handlers[name] = handler


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

    log.info('Reading pipe {}'.format(pipe))

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


def handle_events():

    message_queue = Queue()
    read_pipe(config.APP_RAW_LOG_PIPE, message_queue, parser=parse_raw)

    keep_on_reading = True

    while keep_on_reading:
        try:
            message_event, _exception = message_queue.get_nowait()
            if not _exception:
                for handler in _event_handlers.values():
                    handler(message_event)
            else:
                log.exception(_exception)
        except Empty:
            pass
        time.sleep(0.1)
