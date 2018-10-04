import csv
import sys
import re
import json


def convert(name):
    name = name.replace(' ', '')
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def run():
    with open(sys.argv[1], 'rb') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            message = {convert(k): v for k, v in row.iteritems()}
            print json.dumps(message)


if __name__ == "__main__":
    run()
