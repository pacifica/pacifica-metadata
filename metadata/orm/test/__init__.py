#!/usr/bin/python
"""
This tests the ORM data base objects with sqlite backend
"""
from peewee import SqliteDatabase

DB = SqliteDatabase('people.db')
