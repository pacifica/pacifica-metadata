#!/usr/bin/python

from peewee import PostgresqlDatabase as pgdb
from peewee import Model, DateTimeField
from datetime.datetime import now
from os import getenv

DB = pgdb(os.getenv('POSTGRES_ENV_POSTGRES_DB'),
          user=os.getenv('POSTGRES_ENV_POSTGRES_USER'),
          password=os.getenv('POSTGRES_ENV_POSTGRES_PASSWORD'),
          host=os.getenv('POSTGRES_PORT_5432_TCP_ADDR'),
          port=os.getenv('POSTGRES_PORT_5432_TCP_PORT')
         )

class PacificaModel(Model):
    last_change_date = DateTimeField(default=now)
    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)
    deleted = DateTimeField(default=now)

    class Meta(object):
        database = DB

