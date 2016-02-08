#!/usr/bin/python

from peewee import PostgresqlDatabase as pgdb
from peewee import Model, DateTimeField, Expression, OP, DoesNotExist
from datetime import datetime
from time import mktime
from os import getenv
from json import dumps, loads
from cherrypy import request, HTTPError

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

    def to_hash(self):
        obj = {}
        obj['last_change_date'] = int(mktime(self.last_change_date.timetuple()))
        obj['created'] = int(mktime(self.created.timetuple()))
        obj['updated'] = int(mktime(self.updated.timetuple()))
        obj['deleted'] = int(mktime(self.deleted.timetuple()))
        return obj

    def from_hash(self, obj):
        if 'created' in obj:
            self.created = datetime.fromtimestamp(obj['created'])
        if 'updated' in obj:
            self.updated = datetime.fromtimestamp(obj['updated'])
        if 'last_change_date' in obj:
            self.last_change_date = datetime.fromtimestamp(obj['last_change_date'])
        if 'deleted' in obj:
            self.deleted = datetime.fromtimestamp(obj['deleted'])

    def from_json(self, json_str):
        self.from_hash(loads(json_str))

    def to_json(self):
        return dumps(self.to_hash())

    def where_clause(self, kwargs):
        my_class = self.__class__
        where_clause = Expression(1, OP.EQ, 1)
        for date in ['deleted', 'updated', 'created', 'last_change_date']:
            if date in kwargs:
                kwargs[date] = datetime.fromtimestamp(kwargs[date])
                where_clause &= Expression(my_class.__dict__[date].field, OP.EQ, kwargs[date])
        return where_clause

    exposed = True

    def GET(self, *args, **kwargs):
        try:
            obj = self.get(self.where_clause(kwargs))
        except DoesNotExist, ex:
            raise HTTPError(404, str(ex))
        return obj.to_json()

    def POST(self, *args, **kwargs):
        print kwargs
        try:
            obj = self.get(self.where_clause(kwargs))
        except DoesNotExist, ex:
            raise HTTPError(404, str(ex))
        obj.from_json(request.body.read())
        obj.updated = datetime.now()
        obj.last_change_date = datetime.now()
        obj.save()

    def PUT(self):
        self.from_json(request.body.read())
        self.deleted = datetime.fromtimestamp(0)
        self.updated = datetime.now()
        self.created = datetime.now()
        self.last_change_date = datetime.now()
        self.save()

    def DELETE(self, person_id=-1):
        obj.self.get(person_id=person_id).where(deleted!=0)[0]
        obj.deleted = datetime.now()
        obj.save()
