#!/usr/bin/python
"""
Core interface for each ORM object to interface with CherryPy
"""
from json import loads, dumps
from datetime import datetime
from cherrypy import request, HTTPError
from peewee import DoesNotExist, IntegrityError
from metadata.orm.base import PacificaModel
from metadata.elastic.orm import ElasticAPI
from metadata.orm.utils import datetime_now_nomicrosecond

class CherryPyAPI(PacificaModel, ElasticAPI):
    """
    Core CherryPy interface for all orm objects
    """
    exposed = True

    def _select(self, **kwargs):
        """
        Internal select method.
        """
        objs = self.select().where(self.where_clause(kwargs))
        return dumps([obj.to_hash() for obj in objs])

    def _update(self, update_json, **kwargs):
        """
        Internal update method for an object.
        """
        objs = self.select().where(self.where_clause(kwargs))
        for obj in objs:
            try:
                obj.from_json(update_json)
            except ValueError, ex:
                raise HTTPError(500, str(ex))
            obj.updated = datetime_now_nomicrosecond()
            try:
                self.elastic_upload(obj)
            except Exception, ex:
                raise HTTPError(500, str(ex))
            try:
                obj.save()
            except IntegrityError, ex:
                obj.rollback()
                raise HTTPError(500, str(ex))

    def _set_or_create(self, insert_json):
        """
        Set or create the object if it doesn't already exist
        """
        objs = None
        try:
            objs = loads(insert_json)
        except ValueError, ex:
            raise HTTPError(500, str(ex))
        if isinstance(objs, dict):
            objs = [objs]
        for obj in objs:
            self.from_hash(obj)
            try:
                self.save(force_insert=True)
                self.created = datetime_now_nomicrosecond()
                self.save()
            except IntegrityError, ex:
                self.rollback()
            self.deleted = datetime.fromtimestamp(0)
            self.updated = datetime_now_nomicrosecond()
            self.save()
            try:
                self.elastic_upload(self)
            except Exception, ex:
                raise HTTPError(500, str(ex))

    def _insert(self, insert_json):
        """
        Insert object from json into the system.
        """
        objs = None
        try:
            objs = loads(insert_json)
        except ValueError, ex:
            raise HTTPError(500, str(ex))
        if isinstance(objs, dict):
            objs = [objs]
        for obj in objs:
            self.from_hash(obj)
            self.deleted = datetime.fromtimestamp(0)
            self.updated = datetime_now_nomicrosecond()
            self.created = datetime_now_nomicrosecond()
            try:
                self.save(force_insert=True)
            except IntegrityError, ex:
                self.rollback()
                raise HTTPError(500, str(ex))
            try:
                self.elastic_upload(self)
            except Exception, ex:
                raise HTTPError(500, str(ex))

    def _delete(self, **kwargs):
        """
        Internal delete object method.
        """
        try:
            objs = self.select().where(self.where_clause(kwargs))
        except DoesNotExist, ex:
            raise HTTPError(404, str(ex))
        for obj in objs:
            # also set updated
            obj.deleted = datetime_now_nomicrosecond()
            try:
                self.elastic_delete(obj.to_hash()['_id'])
            except Exception, ex:
                raise HTTPError(500, str(ex))
            try:
                obj.save()
            except IntegrityError, ex:
                obj.rollback()
                raise HTTPError(500, str(ex))

    # CherryPy requires these named methods
    # Add HEAD (basically Get without returning body
    # pylint: disable=invalid-name
    def GET(self, **kwargs):
        """
        Implements the GET HTTP method. Returns the json object based on
        fields passed into kwargs.
        """
        return self._select(**kwargs)

    def PUT(self):
        """
        Implements the PUT HTTP method. Creates an object based on the
        request body.
        """
        self._insert(request.body.read())

    def POST(self, **kwargs):
        """
        Implements the POST HTTP method. Gets the object similar to GET()
        and uses the request body to update the object and saves it.
        """
        self._update(request.body.read(), **kwargs)

    def DELETE(self, **kwargs):
        """
        Implements the DELETE HTTP method. Gets a single object based on
        kwargs, sets the deleted flag and saves the object.
        """
        self._delete(**kwargs)

    # pylint: enable=invalid-name
