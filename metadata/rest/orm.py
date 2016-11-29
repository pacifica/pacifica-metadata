#!/usr/bin/python
"""Core interface for each ORM object to interface with CherryPy."""
from json import loads, dumps
from cherrypy import request, HTTPError
from peewee import IntegrityError, DoesNotExist
from metadata.orm.base import PacificaModel
from metadata.elastic.orm import ElasticAPI
from metadata.orm.utils import datetime_now_nomicrosecond


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
        objs = self.select().where(self.where_clause(kwargs))
        complete_objs = []
        for obj in objs:
            try:
                obj.from_json(update_json)
            except ValueError as ex:
                raise HTTPError(500, str(ex))
            if obj.updated is None:
                obj.updated = datetime_now_nomicrosecond()
            try:
                obj.save()
            except IntegrityError as ex:  # pragma no cover
                obj.rollback()
                raise HTTPError(500, str(ex))
            complete_objs.append(obj.to_hash())
        self.elastic_upload(complete_objs)

    def _set_or_create(self, insert_json):
        """Set or create the object if it doesn't already exist."""
        objs = None
        try:
            objs = loads(insert_json)
        except ValueError as ex:
            raise HTTPError(500, str(ex))
        if isinstance(objs, dict):
            objs = [objs]
        complete_objs = []
        for obj in objs:
            self.from_hash(obj)
            try:
                self.save(force_insert=True)
                self.created = datetime_now_nomicrosecond()
            except IntegrityError as ex:
                self.rollback()
            self.deleted = None
            self.updated = datetime_now_nomicrosecond()
            self.save()
            complete_objs.append(self.to_hash())
        self.elastic_upload(complete_objs)

    def _insert(self, insert_json):
        """Insert object from json into the system."""
        objs = None
        try:
            objs = loads(insert_json)
        except ValueError as ex:
            raise HTTPError(500, str(ex))
        if isinstance(objs, dict):
            objs = [objs]
        bad_id_list = self.__class__.check_for_key_existence(objs)
        if len(bad_id_list) > 0:
            message = 'Could not insert records [ID: {0}] due to duplicated ID values. '.format(','.join(bad_id_list))
            message += 'Remove or change the duplicated id values'
            raise HTTPError(400, message)
        clean_objs = self._clean_for_bulk_upload(objs)
        es_objs = []
        insert_query = self.__class__.insert_many(clean_objs['upload_objs']).returning(self.__class__)
        with self.__class__.atomic():
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

    def _clean_for_bulk_upload(self, obj_hashes):
        model_info = self.__class__.get_object_info()
        clean_objs = {'es_objs': [], 'upload_objs': []}
        for obj in obj_hashes:
            # if 'id' in obj.keys():
            #     obj['_id'] = obj['id']
            if '_id' in obj.keys():
                obj['id'] = obj['_id']
            self.from_hash(obj)
            self.deleted = None
            self.created = self.updated
            new_obj = self.to_hash()
            es_obj = self.to_hash()
            clean_objs['es_objs'].append(es_obj)

            if len(model_info.get('related_models')) > 0:
                rel_models = model_info.get('related_models')
                for (name, info) in rel_models.iteritems():
                    # replace incoming lookup table names with
                    # corresponding model field names
                    db_col = info.get('db_column')
                    if db_col in new_obj.keys():
                        new_obj[name] = new_obj.pop(db_col)
            if '_id' in obj.keys():
                if obj['_id'] is not None:
                    new_obj['id'] = obj.get('_id')
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
    def GET(self, **kwargs):
        """
        Implement the GET HTTP method.

        Returns the json object based on fields passed into kwargs.
        """
        return self._select(**kwargs)

    def PUT(self):
        """
        Implement the PUT HTTP method.

        Creates an object based on the request body.
        """
        self._insert(request.body.read())

    def POST(self, **kwargs):
        """
        Implement the POST HTTP method.

        Gets the object similar to GET() and uses the request body to update
        the object and saves it.
        """
        self._update(request.body.read(), **kwargs)

    def DELETE(self, **kwargs):
        """
        Implement the DELETE HTTP method.

        Gets a single object based on kwargs, sets the deleted flag and saves
        the object.
        """
        self._delete(**kwargs)

    # pylint: enable=invalid-name
