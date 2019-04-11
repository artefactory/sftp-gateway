import sys


def reraise():
    exc_info = sys.exc_info()
    raise exc_info[0], exc_info[1], exc_info[2]
