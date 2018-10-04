import os
import sys
import base64
import re

env_prefix = r'^GCSSFTP_'
file_suffix = r'_FILE$'


def make():
    values = {k: os.environ[k] for k in os.environ if re.search(env_prefix, k)}

    for f in [f for f in values if re.search(file_suffix, f)]:
        key = re.sub(file_suffix, '', f)
        values[key] = base64.b64encode(open(os.environ[f], 'r').read())
        del(values[f])

    for key, var in values.iteritems():
        sys.stdout.write(key)
        sys.stdout.write("=")
        sys.stdout.write(var)
        sys.stdout.write("\n")


if __name__ == '__main__':
    make()
