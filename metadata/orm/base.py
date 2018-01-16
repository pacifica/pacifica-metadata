#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Pacifica Metadata ORM Base Class.

This class implements the basic functionality needed for all
metadata objects in the metadata model for Pacifica.

PacificaModel.

Base class inherits from the PeeWee ORM Model class to create
required fields by all objects and serialization methods for
the base fields.

There are also CherryPy methods for creating, updating, getting
and deleting these objects in from a web service layer.
"""
from os import getenv
from json import dumps, loads
import logging
from peewee import PostgresqlDatabase as pgdb
from peewee import Model, Expression, OP, PrimaryKeyField, fn
from peewee import CompositeKey, R, Clause, ReverseRelationDescriptor

from metadata.orm.utils import index_hash, ExtendDateTimeField
from metadata.orm.utils import datetime_converts, date_converts, datetime_now_nomicrosecond

# Primary PeeWee database connection object constant
DB = pgdb(getenv('POSTGRES_ENV_POSTGRES_DB', 'pacifica_metadata'),
          user=getenv('POSTGRES_ENV_POSTGRES_USER', 'pacifica'),
          password=getenv('POSTGRES_ENV_POSTGRES_PASSWORD', 'pacifica'),
          host=getenv('POSTGRES_PORT_5432_TCP_ADDR', 'localhost'),
          port=int(getenv('POSTGRES_PORT_5432_TCP_PORT', 5432)))

DEFAULT_ELASTIC_ENDPOINT = getenv(
    'ELASTICDB_PORT', 'tcp://127.0.0.1:9200').replace('tcp', 'http')
ELASTIC_ENDPOINT = getenv('ELASTIC_ENDPOINT', DEFAULT_ELASTIC_ENDPOINT)

# Print all queries to stderr.
# pylint: disable=invalid-name
logger = logging.getLogger('peewee')
# pylint: enable=invalid-name
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())


def db_connection_decorator(func):
    """Wrap a method with a database connect and close."""
    def func_wrapper(*args, **kwargs):
        """Wrapper to connect and close connection to database."""
        if DB.is_closed():
            DB.connect()
        try:
            with DB.transaction():
                ret = func(*args, **kwargs)
        finally:
            DB.close()
        return ret
    return func_wrapper


class PacificaModel(Model):
    """
    Basic fields for an object within the model.

    Attributes:
        +-------------------+-------------------------------------+
        | Name              | Description                         |
        +===================+=====================================+
        | created           | When was the object created         |
        +-------------------+-------------------------------------+
        | updated           | When was the object last changed    |
        +-------------------+-------------------------------------+
        | deleted           | When was the object deleted         |
        +-------------------+-------------------------------------+
    """

    # this is peewee specific need to disable this check
    # pylint: disable=invalid-name
    id = PrimaryKeyField()
    # pylint: enable=invalid-name
    created = ExtendDateTimeField(
        default=datetime_now_nomicrosecond, index=True)
    updated = ExtendDateTimeField(
        default=datetime_now_nomicrosecond, index=True)
    deleted = ExtendDateTimeField(null=True, index=True)

    # pylint: disable=too-few-public-methods
    class Meta(object):
        """PeeWee meta class contains the db connection."""

        database = DB
        only_save_dirty = True
    # pylint: enable=too-few-public-methods

    def _set_only_if(self, key, obj, dest_attr, func):
        if key in obj:
            setattr(self, dest_attr, func())

    def _set_date_part(self, date_part, obj):
        self._set_only_if(date_part, obj, date_part,
                          lambda: date_converts(obj[date_part]))

    def _set_datetime_part(self, time_part, obj):
        self._set_only_if(time_part, obj, time_part,
                          lambda: datetime_converts(obj[time_part]))

    @classmethod
    def cls_foreignkeys(cls):
        """Provide the foreign keys of the class as a list of attrs."""
        # pylint: disable=no-member
        return cls._meta.rel.keys()
        # pylint: enable=no-member

    @classmethod
    def cls_foreignkey_rel_mods(cls):
        """Return a collection of related models for a given foreignkey."""
        # pylint: disable=no-member
        return {cls._meta.rel[fk].rel_model: fk for fk in cls._meta.rel}
        # pylint: enable=no-member

    @classmethod
    def cls_revforeignkeys(cls):
        """Provide the rev foreign keys of the class as a list of attrs."""
        ret = []
        for attr, value in cls.__dict__.items():
            if isinstance(value, ReverseRelationDescriptor):
                ret.append(attr)
        return ret

    def to_hash(self, **flags):
        """Convert the base object fields into serializable attributes in a hash."""
        recursion_depth = flags.get('recursion_depth', 0)
        obj = {}
        obj['created'] = self.created.isoformat()
        obj['updated'] = self.updated.isoformat()
        obj['deleted'] = self.deleted.isoformat(
        ) if self.deleted is not None else None
        obj['_id'] = index_hash(obj['created'], obj['updated'], obj['deleted'])
        if recursion_depth:
            for attr in set(self.cls_revforeignkeys()) - set(flags.get('recursion_exclude', [])):
                rec_flags = flags.copy()
                rec_flags['recursion_depth'] -= 1
                obj.update(self._build_object(attr))

        return obj

    def _build_object(self, attr):
        obj = {attr: []}

        for obj_ref in getattr(self, attr):
            if not fk_obj_list:
                fk_item_name, fk_obj_list = self._generate_fk_obj_list(obj_ref)

            if 'key' in fk_obj_list.values() and 'value' in fk_obj_list.values():
                obj[attr].append(
                    {
                        'key_id': obj_ref._data['key'],
                        'value_id': obj_ref._data['value']
                    }
                )
            else:
                # pylint: disable=protected-access
                obj[attr].append(obj_ref._data[fk_item_name])
                # pylint: enable=protected-access
        return obj

    def _generate_fk_obj_list(self, obj_ref):
        fk_obj_list = obj_ref.cls_foreignkey_rel_mods()
        valid_fk_obj_list = list(
            set(fk_obj_list) - set([self.__class__]))
        if len(valid_fk_obj_list) == 1:
            fk_item_name = fk_obj_list[valid_fk_obj_list.pop()]
        else:
            fk_item_name = 'id'
        return fk_item_name, fk_obj_list

    def from_hash(self, obj):
        """Convert the hash objects into object fields if they are present."""
        self._set_datetime_part('created', obj)
        self._set_datetime_part('updated', obj)
        self._set_datetime_part('deleted', obj)

    def from_json(self, json_str):
        """Convert the json string into the current object."""
        if not isinstance(loads(json_str), dict):
            raise ValueError('json_str not dict')
        self.from_hash(loads(json_str))

    def to_json(self):
        """Convert the object into a json object."""
        return dumps(self.to_hash())

    @staticmethod
    def _bool_translate(thing):
        """Translate the thing into a boolean."""
        return False if str(thing).lower() == 'false' else bool(thing)

    @staticmethod
    def _date_operator_compare(date, kwargs, dt_converts=datetime_converts):
        if '{0}_operator'.format(date) in kwargs:
            date_oper = getattr(
                OP, kwargs['{0}_operator'.format(date)].upper())
        else:
            date_oper = OP.EQ
        if date_oper == OP.BETWEEN:
            date_obj_min = dt_converts(kwargs[date][0])
            date_obj_max = dt_converts(kwargs[date][1])
            date_obj = Clause(date_obj_min, R('AND'), date_obj_max)
        else:
            date_obj = dt_converts(kwargs[date])
        return (date_obj, date_oper)

    def where_clause(self, kwargs):
        """PeeWee specific extension meant to be passed to a PeeWee get or select."""
        my_class = self.__class__
        where_clause = Expression(1, OP.EQ, 1)
        if 'deleted' in kwargs:
            if kwargs['deleted'] is None:
                where_clause &= Expression(
                    getattr(my_class, 'deleted'), OP.IS, None)
            else:
                date_obj = datetime_converts(kwargs['deleted'])
                where_clause &= Expression(
                    getattr(my_class, 'deleted'), OP.EQ, date_obj)
        for date in ['updated', 'created']:
            if date in kwargs:
                # pylint: disable=protected-access
                date_obj, date_oper = my_class._date_operator_compare(
                    date, kwargs)
                # pylint: enable=protected-access
                where_clause &= Expression(
                    getattr(my_class, date), date_oper, date_obj)
        return where_clause

    @classmethod
    def _where_attr_clause(cls, where_clause, kwargs, keys):
        """Grab keys and operators out of kwargs and return where clause."""
        for key in keys:
            if key in kwargs:
                key_oper = OP.EQ
                if '{0}_operator'.format(key) in kwargs:
                    key_oper = getattr(
                        OP, kwargs['{0}_operator'.format(key)].upper())
                where_clause &= Expression(
                    getattr(cls, key), key_oper, kwargs[key])
        return where_clause

    @classmethod
    def last_change_date(cls):
        """Find the last changed date for the object."""
        last_change_date = cls.select(fn.Max(cls.updated)).scalar()
        return last_change_date.isoformat(' ') if last_change_date is not None else '1970-01-01 00:00:00'

    @classmethod
    def available_hash_list(cls):
        """
        Generate a hashable structure of all keys and values of keys.

        This structure allows for easy evaluation of updates or current vs old data
        for any object in the database.
        """
        hash_list = []
        hash_dict = {}
        all_keys_query = cls.select(*[getattr(cls, key)
                                      for key in cls.get_primary_keys()]).dicts()
        for obj in all_keys_query.execute():
            inst_key = index_hash(*obj.values())
            hash_list.append(inst_key)
            entry = {
                'key_list': obj,
                'index_hash': inst_key
            }
            hash_dict[inst_key] = entry
        return hash_list, hash_dict

    @classmethod
    def get_primary_keys(cls):
        """Return the primary keys for the object."""
        # pylint: disable=no-member
        primary_key = cls._meta.primary_key
        if isinstance(primary_key, CompositeKey) and cls._meta.rel:
            return list(primary_key.field_names)
        # pylint: enable=no-member
        return [primary_key.name]

    @classmethod
    def get_object_info(cls):
        """Get model and field information about the model class."""
        last_changed = cls.last_change_date()
        related_model_info = {}
        # pylint: disable=no-member
        for rel_mod_name in cls._meta.rel:
            if rel_mod_name != cls.__name__:
                fkf = cls._meta.rel.get(rel_mod_name)
                rel_mod = fkf.rel_model
                # pylint: disable=protected-access
                table = rel_mod._meta.db_table
                pkey = rel_mod._meta.primary_key.name
                # pylint: enable=protected-access
                related_model_info[rel_mod_name] = {
                    'db_column': fkf.db_column,
                    'db_table': table,
                    'primary_key': pkey
                }
        js_object = {
            'callable_name': cls.__module__.split('.')[2],
            'last_changed_date': last_changed,
            'primary_keys': cls.get_primary_keys(),
            'field_list': cls._meta.sorted_field_names,
            'foreign_keys': cls.cls_foreignkeys(),
            'related_models': related_model_info,
            'related_names': cls.cls_revforeignkeys(),
            'record_count': cls.select().count()
        }
        # pylint: enable=no-member
        return js_object
