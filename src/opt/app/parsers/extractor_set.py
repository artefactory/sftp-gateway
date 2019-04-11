from parsers.context import context_for


class ExtractorSet(object):

    def __init__(self, process, extractors):
        self.process = process
        self.extractors = extractors

    def apply(self, pid, message):
        messages = []
        clear_context_keys = []

        for extractor in self.extractors:
            extract = extractor.apply(pid, message)
            if extract:
                severity, pmessage, labels = extract
                messages.append(self._make_message(pid, severity, pmessage, labels))
                clear_context_keys += extractor.clear_context_keys

        messages.append(self._make_message(pid, 'debug', message))

        ctx = context_for(pid)
        for key in clear_context_keys:
            if key in ctx:
                del(ctx[key])

        return messages

    def _make_message(self, pid, severity, message, labels={}):
        merged = dict(context_for(pid), **labels)
        merged.update({'process': self.process})
        return (severity, message, merged)
