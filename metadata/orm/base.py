#!/usr/bin/python

from peewee import PostgresqlDatabase as pgdb
from peewee import Model, DateTimeField
from datetime import datetime
from os import getenv

DB = pgdb(getenv('POSTGRES_ENV_POSTGRES_DB'),
          user=getenv('POSTGRES_ENV_POSTGRES_USER'),
          password=getenv('POSTGRES_ENV_POSTGRES_PASSWORD'),
          host=getenv('POSTGRES_PORT_5432_TCP_ADDR'),
          port=getenv('POSTGRES_PORT_5432_TCP_PORT')
         )

class PacificaModel(Model):
    last_change_date = DateTimeField(default=datetime.now)
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)
    deleted = DateTimeField(default=datetime.now)

    class Meta(object):
        database = DB

