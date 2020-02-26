"""Summary
"""
import fnmatch

import config


def is_tmp(path: str):
    """Summary

    Args:
        path (str): Description

    Returns:
        bool: Description
    """
    filters = config.APP_LANDING_TEMP_PATTERNS.split(",")
    return any([fnmatch.fnmatch(path, _filter) for _filter in filters])
