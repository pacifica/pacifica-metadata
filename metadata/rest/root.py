#!/usr/bin/python
"""CherryPy root object class."""
from metadata.orm import ORM_OBJECTS
from metadata.rest.uploader import UploaderAPI


# pylint: disable=too-few-public-methods
class Root(object):
    """
    CherryPy root object class.

    not exposed by default the base objects are exposed
    """

    exposed = False
    uploader = UploaderAPI
# pylint: enable=too-few-public-methods


for cls in ORM_OBJECTS:
    # this is based on the module name being something like metadata.orm.BLAH
    obj_loc = cls.__module__.split('.')[2]
    setattr(Root, obj_loc, cls())
