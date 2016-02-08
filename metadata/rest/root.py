#!/usr/bin/python

from metadata.orm.users import Users

class Root(object):
    exposed = False
    users = Users()

