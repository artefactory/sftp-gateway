import json


def parse_syncer(pid, raw_message):

    messages = []

    try:
        parsed_json = json.loads(raw_message)
        labels = parsed_json.get('labels', {})

        labels.update({
            'process': 'syncer'
        })
        #
        # if parsed_json['result'] == 'OK':
        #     message = "{} sucessfully uploaded to {}".format(filename, parsed_json['destination'])
        #     severity = "info"
        #     labels['event'] = 'upload_succeeded'
        #
        # elif parsed_json['result'] == "skip":
        #     message = "{} skipped, already present on destination".format(filename)
        #     severity = "warn"
        #     labels['event'] = 'upload_skipped'
        #
        # else:
        #     message = "Error: {}".format(parsed_json['description'])
        #     severity = "error"
        #     labels['event'] = 'error'

        messages.append((parsed_json['severity'], parsed_json['message'], labels))

    except Exception as ex:
        messages.append(('error', 'Error parsing JSON log event', {}))
        messages.append(('error', 'Exception: {}'.format(ex.message), {}))
        messages.append(('error', 'Message: {}'.format(raw_message), {}))

    return messages
