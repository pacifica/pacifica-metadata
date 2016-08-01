#!/usr/bin/python
"""
Utilities for common metadata tools.
"""
from hashlib import md5
from datetime import datetime, date
from peewee import DateTimeField, DateField
from dateutil import parser


def index_hash(*args):
    """
    Generate a hash for all the arguments passed.

    This is used to combine multiple unique IDs into a single string.
    """
    arg_hash = md5()
    for arg in args:
        arg_hash.update(str(arg))
    return arg_hash.hexdigest()


def date_converts(date_obj):
    """
    Standardize on converting to date objects
    """
    if isinstance(date_obj, str) or isinstance(date_obj, unicode):
        return parser.parse(date_obj).date()
    elif isinstance(date_obj, date):
        return date_obj
    elif isinstance(date_obj, int):
        return datetime.fromtimestamp(date_obj).date()


def datetime_now_nomicrosecond():
    """
    return now with no microseconds
    """
    return datetime.now().replace(microsecond=0)


def datetime_converts(time_obj):
    """
    Standardize on converting to datetime objects
    """
    if isinstance(time_obj, str) or isinstance(time_obj, unicode):
        return parser.parse(time_obj).replace(microsecond=0)
    elif isinstance(time_obj, datetime):
        return time_obj.replace(microsecond=0)
    elif isinstance(time_obj, int):
        return datetime.fromtimestamp(time_obj).replace(microsecond=0)


class ExtendDateTimeField(DateTimeField):
    """
    Appends to the DateTimeField to add isoformat from datetime object
    """

    def isoformat(self):
        """
        return the isoformat datetime field
        """
        return datetime(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second
        ).isoformat()


class ExtendDateField(DateField):
    """
    Appends to the DateField to add isoformatted date
    """

    def isoformat(self):
        """
        return the isoformat date field
        """
        return date(
            self.year,
            self.month,
            self.day
        ).strftime('%Y-%m-%d')
