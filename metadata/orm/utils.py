#!/usr/bin/python
"""
Utilities for common metadata tools.
"""
from hashlib import md5

def index_hash(*args):
    """
    Generate a hash for all the arguments passed.

    This is used to combine multiple unique IDs into a single string.
    """
    arg_hash = md5()
    for arg in args:
        arg_hash.update(str(arg))
    return arg_hash.hexdigest()
