import os
import pystache


def render_config(path, to_update):
    result = {}
    with open(path, "r") as f:
        for line in f.read().split("\n"):
            if len(line.strip()) > 0 and line.strip()[0] != "#":
                os.environ[line.split('=')[0]] = pystache.render(''.join(line.split('=')[1:]), dict(os.environ)).strip("\'")
                result[line.split('=')[0]] = os.environ[line.split('=')[0]]
    to_update.update(result)
