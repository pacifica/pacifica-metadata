#!/usr/bin/python
"""Core interface for each ORM object to interface with CherryPy."""
from json import loads, dumps
from cherrypy import request, HTTPError
from peewee import DoesNotExist
from metadata.orm.base import PacificaModel, db_connection_decorator
from metadata.elastic.orm import ElasticAPI
from metadata.orm.utils import datetime_now_nomicrosecond, datetime_converts


class CherryPyAPI(PacificaModel, ElasticAPI):
    """Core CherryPy interface for all orm objects."""

    exposed = True

    def _select(self, **kwargs):
        """Internal select method."""
        primary_keys = []
        for key in self.get_primary_keys():
            primary_keys.append(getattr(self.__class__, key))
        objs = (self.select()
                .where(self.where_clause(kwargs))
                .order_by(*primary_keys))
        if 'page_number' in kwargs and 'items_per_page' in kwargs:
            objs = objs.paginate(int(kwargs['page_number']), int(kwargs['items_per_page']))
        return dumps([obj.to_hash() for obj in objs])

    def _update(self, update_json, **kwargs):
        """Internal update method for an object."""
        update_hash = loads(update_json)
        if 'updated' not in update_hash:
            update_hash['updated'] = datetime_now_nomicrosecond()
        did_something = False
        for obj in self.select().where(self.where_clause(kwargs)):
            did_something = True
            obj.from_hash(update_hash)
            obj.save()
        if not did_something:
            raise HTTPError(500, "Get args didn't select any objects.")
        complete_objs = [obj.to_hash() for obj in self.select().where(self.where_clause(kwargs))]
        self.elastic_upload(complete_objs)

    def _set_or_create(self, insert_json):
        """Set or create the object if it doesn't already exist."""
        objs = loads(insert_json)
        if isinstance(objs, dict):
            objs = [objs]
        complete_objs = []
        for obj_hash in objs:
            if '_id' in obj_hash:
                obj_hash['id'] = obj_hash.pop('_id')
            obj, created = self.get_or_create(**obj_hash)
            if created:
                complete_objs.append(obj.to_hash())
        self.elastic_upload(complete_objs)

    def _insert(self, insert_json):
        """Insert object from json into the system."""
        objs = loads(insert_json)
        if not objs:
            # nothing to upload
            return
        if isinstance(objs, dict):
            objs = [objs]
        bad_id_list = self.__class__.check_for_key_existence(objs)
        if bad_id_list:
            message = 'Could not insert records [ID: {0}] due to duplicated ID values. '.format(','.join(bad_id_list))
            message += 'Remove or change the duplicated id values'
            raise HTTPError(400, message)

        def fix_dates(orig_obj, db_obj, es_obj):
            """Fix the dates for insert."""
            for date_key in ['created', 'updated', 'deleted']:
                if date_key in orig_obj:
                    es_obj[date_key] = db_obj[date_key] = datetime_converts(orig_obj[date_key])
            for date_key in ['created', 'updated']:
                if date_key not in orig_obj:
                    es_obj[date_key] = db_obj[date_key] = datetime_converts(datetime_now_nomicrosecond())
            if 'deleted' not in orig_obj:
                db_obj['deleted'] = es_obj['deleted'] = None
        clean_objs = self._clean_for_bulk_upload(objs, fix_dates)
        es_objs = []
        insert_query = self.__class__.insert_many(clean_objs['upload_objs']).returning(self.__class__)
        for item in insert_query.execute():
            es_objs.append(item.to_hash())
        self.elastic_upload(es_objs)

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

    def _clean_for_bulk_upload(self, obj_hashes, fix_dates):
        model_info = self.__class__.get_object_info()
        clean_objs = {'es_objs': [], 'upload_objs': []}
        for obj in obj_hashes:
            if '_id' in obj.keys():
                obj['id'] = obj['_id']
            self.from_hash(obj)
            new_obj = self.to_hash()
            es_obj = self.to_hash()
            fix_dates(obj, new_obj, es_obj)
            clean_objs['es_objs'].append(es_obj)

            if model_info.get('related_models'):
                rel_models = model_info.get('related_models')
                for (name, info) in rel_models.items():
                    # replace incoming lookup table names with
                    # corresponding model field names
                    db_col = info.get('db_column')
                    if db_col in new_obj.keys():
                        new_obj[name] = new_obj.pop(db_col)
            if '_id' in obj.keys() and obj['_id'] is not None:
                new_obj['id'] = obj.get('_id')
            for attr in model_info.get('related_names'):
                del new_obj[attr]
            new_obj.pop('_id')
            clean_objs['upload_objs'].append(new_obj)

        return clean_objs

    def _delete(self, **kwargs):
        """Internal delete object method."""
        update_hash = {
            'deleted': datetime_now_nomicrosecond().isoformat()
        }
        self._update(dumps(update_hash), **kwargs)

    # CherryPy requires these named methods
    # Add HEAD (basically Get without returning body
    # pylint: disable=invalid-name

    @db_connection_decorator
    def GET(self, **kwargs):
        """
        Implement the GET HTTP method.

        Returns the json object based on fields passed into kwargs.
        """
        return self._select(**kwargs)

    @db_connection_decorator
    def PUT(self):
        """
        Implement the PUT HTTP method.

        Creates an object based on the request body.
        """
        self._insert(request.body.read())

    @db_connection_decorator
    def POST(self, **kwargs):
        """
        Implement the POST HTTP method.

        Gets the object similar to GET() and uses the request body to update
        the object and saves it.
        """
        self._update(request.body.read(), **kwargs)

    @db_connection_decorator
    def DELETE(self, **kwargs):
        """
        Implement the DELETE HTTP method.

        Gets a single object based on kwargs, sets the deleted flag and saves
        the object.
        """
        self._delete(**kwargs)

    # pylint: enable=invalid-name
