#!/usr/bin/python

from peewee import PostgresqlDatabase as pgdb
from os import getenv

DB = pgdb(os.getenv('POSTGRES_ENV_POSTGRES_DB'),
          user=os.getenv('POSTGRES_ENV_POSTGRES_USER'),
          password=os.getenv('POSTGRES_ENV_POSTGRES_PASSWORD'),
          host=os.getenv('POSTGRES_PORT_5432_TCP_ADDR'),
          port=os.getenv('POSTGRES_PORT_5432_TCP_PORT')
         )
