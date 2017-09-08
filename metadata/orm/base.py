#!/usr/bin/python
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
from peewee import PostgresqlDatabase as pgdb, ReverseRelationDescriptor
from peewee import Model, Expression, OP, PrimaryKeyField, fn, CompositeKey, R, Clause

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
    created = ExtendDateTimeField(default=datetime_now_nomicrosecond, index=True)
    updated = ExtendDateTimeField(default=datetime_now_nomicrosecond, index=True)
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

    def to_hash(self):
        """Convert the base object fields into serializable attributes in a hash."""
        obj = {}
        obj['created'] = self.created.isoformat()
        obj['updated'] = self.updated.isoformat()
        obj['deleted'] = self.deleted.isoformat() if self.deleted is not None else None
        obj['_id'] = index_hash(obj['created'], obj['updated'], obj['deleted'])
        for attr, value in self.__class__.__dict__.items():
            if isinstance(value, ReverseRelationDescriptor):
                obj[attr] = [obj_id for obj_id in getattr(self, attr)]
        return obj

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
        ret = bool(thing)
        if thing == 'False':
            ret = False
        elif thing == 'false':
            ret = False
        return ret

    @staticmethod
    def _date_operator_compare(date, kwargs, dt_converts=datetime_converts):
        if '{0}_operator'.format(date) in kwargs:
            date_oper = getattr(OP, kwargs['{0}_operator'.format(date)].upper())
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
                date_obj, date_oper = my_class._date_operator_compare(date, kwargs)
                # pylint: enable=protected-access
                where_clause &= Expression(
                    getattr(my_class, date), date_oper, date_obj)
        return where_clause

    @classmethod
    def last_change_date(cls):
        """Find the last changed date for the object."""
        return cls.select(fn.Max(cls.updated)).scalar()

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
        if cls.last_change_date() is not None:
            last_changed = cls.last_change_date().isoformat(' ')
        else:
            last_changed = '1970-01-01 00:00:00'
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
            'foreign_keys': cls._meta.rel.keys(),
            'related_models': related_model_info,
            'record_count': cls.select().count()
        }
        # pylint: enable=no-member
        return js_object
