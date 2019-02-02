#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Core interface for each ORM object to interface with CherryPy."""
import cherrypy
from cherrypy import HTTPError
from peewee import DoesNotExist
from pacifica.metadata.orm.base import PacificaModel, db_connection_decorator
from pacifica.metadata.orm.utils import datetime_now_nomicrosecond, datetime_converts


class CherryPyAPI(PacificaModel):
    """Core CherryPy interface for all orm objects."""

    es_recursive_flags = {
        'recursion_depth': 1,
        'recursion_limit': 1000,
        'recursion_exclude': []
    }
    exposed = True

    def _select(self, **kwargs):
        """Internal select method."""
        primary_keys = []
        copy_flags = self.es_recursive_flags.copy()
        self._set_recursion_depth(copy_flags, kwargs)
        self._set_recursion_limit(copy_flags, kwargs)
        for key in self.get_primary_keys():
            primary_keys.append(getattr(self.__class__, key))
        objs = (self.select()
                .where(self.where_clause(kwargs))
                .order_by(*primary_keys))
        if 'page_number' in kwargs and 'items_per_page' in kwargs:
            objs = objs.paginate(
                int(kwargs['page_number']), int(kwargs['items_per_page']))
        return [obj.to_hash(**copy_flags) for obj in objs]

    @staticmethod
    def _set_recursion_limit(flags, kwargs):
        recursion_limit = int(kwargs.get('recursion_limit', 1000))
        flags['recursion_limit'] = recursion_limit

    @staticmethod
    def _set_recursion_depth(flags, kwargs):
        recursion_depth = int(kwargs.get('recursion_depth', 1))
        if recursion_depth not in range(0, 2):
            raise ValueError('Recursion depth must be in the range of 0->2.')
        flags['recursion_depth'] = recursion_depth

    def _update(self, update_hash, **kwargs):
        """Internal update method for an object."""
        update_hash['updated'] = update_hash.get(
            'updated', datetime_now_nomicrosecond())
        did_something = False
        for obj in self.select().where(self.where_clause(kwargs)):
            did_something = True
            obj.from_hash(update_hash)
            obj.save()
        if not did_something:
            raise HTTPError(500, "Get args didn't select any objects.")

    def _set_or_create(self, objs):
        """Set or create the object if it doesn't already exist."""
        if isinstance(objs, dict):
            objs = [objs]
        for obj_hash in objs:
            if '_id' in obj_hash:
                obj_hash['id'] = obj_hash.pop('_id')
            obj, _created = self.get_or_create(**obj_hash)

    @staticmethod
    def __fix_dates(orig_obj, db_obj):
        """Fix the dates for insert."""
        for date_key in ['created', 'updated', 'deleted']:
            if date_key in orig_obj:
                db_obj[date_key] = datetime_converts(orig_obj[date_key])
        for date_key in ['created', 'updated']:
            if date_key not in orig_obj:
                db_obj[date_key] = datetime_converts(
                    datetime_now_nomicrosecond())
        if 'deleted' not in orig_obj:
            db_obj['deleted'] = None

    def _insert(self, objs):
        """Insert object from json into the system."""
        if not objs:
            # nothing to upload
            return
        if isinstance(objs, dict):
            objs = [objs]
        bad_id_list = self.__class__.check_for_key_existence(objs)
        if bad_id_list:
            message = 'Could not insert records [ID: {0}] due to duplicated ID values. '.format(
                ','.join(bad_id_list))
            message += 'Remove or change the duplicated id values'
            raise HTTPError(400, message)
        clean_objs = self._insert_many_format(objs)
        # pylint: disable=no-value-for-parameter
        self.__class__.insert_many(clean_objs).execute()
        # pylint: enable=no-value-for-parameter

    @classmethod
    def check_for_key_existence(cls, object_list):
        """Check for already loaded keys to prevent collisions."""
        cls_instance = cls()
        bad_id_list = []
        for item in object_list:
            item_id = item['_id'] if '_id' in item.keys() else None
            if item_id is not None:
                try:
                    obj = cls.get(cls_instance.where_clause({'_id': item_id}))
                    bad_id_list.append(obj.id)
                except DoesNotExist:
                    obj = None
        return [str(x) for x in bad_id_list]

    @classmethod
    def _insert_many_format(cls, obj_hashes):
        model_info = cls.get_object_info()
        clean_objs = []
        for obj in obj_hashes:
            cls_obj = cls()
            cls_obj.from_hash(obj)
            db_obj = {}
            for key in set(model_info['field_list']) - set(['id']):
                db_obj[key] = cls_obj.__data__.get(key, None)
            if '_id' in obj:
                db_obj['id'] = obj['_id']
            cls.__fix_dates(obj, db_obj)
            clean_objs.append(db_obj)
        return clean_objs

    def _delete(self, **kwargs):
        """Internal delete object method."""
        update_hash = {
            'deleted': datetime_now_nomicrosecond().isoformat()
        }
        self._update(update_hash, **kwargs)

    # CherryPy requires these named methods
    # Add HEAD (basically Get without returning body
    # pylint: disable=invalid-name

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @db_connection_decorator
    def GET(self, **kwargs):
        """
        Implement the GET HTTP method.

        Returns the json object based on fields passed into kwargs.
        """
        return self._select(**kwargs)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @db_connection_decorator
    def PUT(self):
        """
        Implement the PUT HTTP method.

        Creates an object based on the request body.
        """
        self._insert(cherrypy.request.json)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @db_connection_decorator
    def POST(self, **kwargs):
        """
        Implement the POST HTTP method.

        Gets the object similar to GET() and uses the request body to update
        the object and saves it.
        """
        self._update(cherrypy.request.json, **kwargs)

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @db_connection_decorator
    def DELETE(self, **kwargs):
        """
        Implement the DELETE HTTP method.

        Gets a single object based on kwargs, sets the deleted flag and saves
        the object.
        """
        self._delete(**kwargs)

    # pylint: enable=invalid-name
