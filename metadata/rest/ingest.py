#!/usr/bin/python
"""
Core interface for the ingest of metadata objects.

Example uploaded data:
[
  {"destinationTable": "Transactions._id", "value": 1234},
  {"destinationTable": "Transactions.submitter", "value": 34002},
  {"destinationTable": "Transactions.proposal", "value": 34002},
  {"destinationTable": "Transactions.instrument", "value": 34002},
  {"destinationTable": "TransactionKeyValue", "key": "Tag", "value": "Blah"},
  {"destinationTable": "TransactionKeyValue", "key": "Taggy", "value": "Blah"},
  {"destinationTable": "TransactionKeyValue", "key": "Taggier", "value": "Blah"}
  {
    "destinationTable": "Files",
    "_id": 34, "name": "foo.txt", "subdir": "a/b/",
    "ctime": "Tue Nov 29 14:09:05 PST 2016",
    "mtime": "Tue Nov 29 14:09:05 PST 2016",
    "size": 128, "mimetype": "text/plain"
  },
  {
      "destinationTable": "FileKeyValue",
      "key": "Micronic Adjustment",
      "value": "5.66%",
      "file_id": 34
  },
  {
    "destinationTable": "Files",
    "_id": 35, "name": "bar.txt", "subdir": "a/b/",
    "ctime": "Tue Nov 29 14:09:05 PST 2016",
    "mtime": "Tue Nov 29 14:09:05 PST 2016",
    "size": 47, "mimetype": "text/plain"
  },
]
"""
from __future__ import print_function
from json import dumps
from cherrypy import request, tools
from metadata.orm.transactions import Transactions
from metadata.orm.trans_key_value import TransactionKeyValue
from metadata.orm.file_key_value import FileKeyValue
from metadata.orm.keys import Keys
from metadata.orm.values import Values
from metadata.orm.files import Files


# pylint: disable=too-few-public-methods
class IngestAPI(object):
    """Uploader ingest API."""

    exposed = True

    # CherryPy requires these named methods.
    # pylint: disable=invalid-name
    @staticmethod
    @tools.json_in()
    @tools.json_out()
    def PUT():
        """Sample doc string to put data to the server."""
        def pull_value_by_attr(json, table, attr):
            """Pull a value out of the json hash."""
            return [part[attr] for part in json if part['destinationTable'] == table][0]

        def pull_kv_by_attr(json):
            """Yield key value pairs from the json hash."""
            for part in json:
                if part['destinationTable'] == 'TransactionKeyValue':
                    yield (part['key'], part['value'])

        def pull_fkv_by_attr(json):
            """Yield key values pairs for the file_key_value store from the json hash."""
            for part in json:
                if part['destinationTable'] == 'FileKeyValue':
                    yield (part['key'], part['value'], part['file_id'])

        def pull_file_by_attr(json):
            """Yield the files as a hash from the json hash."""
            for part in json:
                if part['destinationTable'] == 'Files':
                    ret = {}
                    for key in ['name', 'subdir', 'mtime', 'ctime', 'size', 'mimetype', '_id']:
                        ret[key] = part[key]
                    yield ret

        def generate_tkvs(json):
            """Extract TransactionKeyValues as a hash from the json hash."""
            keys = []
            values = []
            tkvs = []
            for key, value in pull_kv_by_attr(json):
                keys.append({'key': key})
                values.append({'value': value})
            # pylint: disable=protected-access
            Keys()._set_or_create(dumps(keys))
            Values()._set_or_create(dumps(values))
            # pylint: enable=protected-access
            for key, value in pull_kv_by_attr(json):
                # key_obj = Keys.get(key=key)
                # value_obj = Values.get(value=value)
                tkvs.append({
                    'key_id': Keys.get(key=key).id,
                    'transaction_id': transaction_hash['_id'],
                    'value_id': Values.get(value=value).id
                })

            return tkvs

        def generate_fkvs(json):
            """Extract FileKeyValues as a hash from the json hash."""
            file_keys = []
            file_values = []
            fkvs = []
            for key, value, file_id in pull_fkv_by_attr(json):
                file_keys.append({'key': key})
                file_values.append({'value': value})

            # pylint: disable=protected-access
            Keys()._set_or_create(dumps(file_keys))
            Values()._set_or_create(dumps(file_values))
            # pylint: enable=protected-access

            for key, value, file_id in pull_fkv_by_attr(json):
                # key_obj =
                # value_obj = Values.get(value=value)
                fkvs.append({
                    'key_id': Keys.get(key=key).id,
                    'value_id': Values.get(value=value).id,
                    'file_id': file_id
                })

            return fkvs

        def extract_files(json):
            """Extract file entries as a hash from the json hash."""
            files = []
            for file_hash in pull_file_by_attr(json):
                file_hash['transaction_id'] = transaction_hash['_id']
                files.append(file_hash)
            return files

        transaction_hash = {
            '_id': pull_value_by_attr(request.json, 'Transactions._id', 'value'),
            'submitter': pull_value_by_attr(request.json, 'Transactions.submitter', 'value'),
            'instrument': pull_value_by_attr(request.json, 'Transactions.instrument', 'value'),
            'proposal': pull_value_by_attr(request.json, 'Transactions.proposal', 'value')
        }
        with Transactions.atomic():
            # pylint: disable=protected-access
            Transactions()._insert(dumps(transaction_hash))
            TransactionKeyValue()._insert(dumps(generate_tkvs(request.json)))
            Files()._insert(dumps(extract_files(request.json)))
            FileKeyValue()._insert(dumps(generate_fkvs(request.json)))
            # pylint: enable=protected-access

        return {'status': 'success'}
