import re
from parsers.context import context_for


class Extractor(object):

    def __init__(self, event, pattern, severity, out,
                 context_keys=[],
                 clear_context_keys=[],
                 fn=None):
        self.event = event
        self.pattern = pattern
        self.out = out
        self.severity = severity
        self.context_keys = context_keys
        self.clear_context_keys = clear_context_keys
        self.fn = fn

    def apply(self, pid, message):
        match = re.match(self.pattern, message)
        if match:
            extracted_values = match.groupdict()
            extracted_values['event'] = self.event
            formatted = self.out.format(**extracted_values)

            ctx = context_for(pid)

            for key in self.context_keys:
                ctx[key] = extracted_values[key]

            transmit = True
            if self.fn:
                transmit = self.fn(pid, message, extracted_values)

            if transmit:
                return self.severity, formatted, extracted_values
