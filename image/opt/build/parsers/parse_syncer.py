import os
import json
from parsers.extractor_set import ExtractorSet

extractors = []
extractor_set = ExtractorSet('syncer', extractors)


def parse_syncer(pid, raw_message):

    messages = []

    messages.append(
        ('debug', raw_message, {'process': 'syncer'})
    )

    try:
        parsed_json = json.loads(raw_message)
        filename = os.path.basename(parsed_json['source'])

        labels = {
            'file': filename,
            'destination': parsed_json['destination'],
            'result': parsed_json['result'],
            'process': 'syncer'
        }

        if parsed_json['result'] == 'OK':
            message = "{} sucessfully uploaded to {}".format(filename, parsed_json['destination'])
            severity = "info"

        elif parsed_json['result'] == "skip":
            message = "{} skipped, already present on destination".format(filename)
            severity = "warn"

        messages.append((severity, message, labels))

    except Exception:
        pass

    return messages
