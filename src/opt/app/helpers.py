import fnmatch

import config


def is_tmp(path):
    _filters = config.APP_LANDING_TEMP_PATTERNS.split(",")
    return any([fnmatch.fnmatch(path, _f) for _f in _filters])
