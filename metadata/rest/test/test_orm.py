#!/usr/bin/python
"""Test the ORM interface CherryPyAPI."""
from json import loads, dumps
import logging
import requests
import cherrypy
from cherrypy.test import helper
from test_files.loadit import main
from docker import Client
from metadata.rest.root import Root
from metadata.orm.keys import Keys
from metadata.orm import create_tables


class TestCherryPyAPI(helper.CPWebCase):
    """Test the CherryPyAPI class."""

    PORT = 8121
    HOST = '127.0.0.1'
    url = 'http://{0}:{1}'.format(HOST, PORT)
    headers = {'content-type': 'application/json'}
    es_container_id = None
    cli = Client()

    # we don't care about covering the testing code
    @classmethod
    def docker_pull(cls, image):  # pragma no cover
        """Docker pull the command does more than the docker pull method in python."""
        images = {}
        for data in cls.cli.pull(image, stream=True):
            data = data.strip()
            done = False
            for line in data.split('\n'):
                line = loads(line)
                if 'id' not in line:
                    if 'Image is up to date' in line['status']:
                        done = True
                else:
                    images[line['id']] = line
            if done:
                break
            done = True
            for value in images.values():
                if 'Pull complete' not in value['status']:
                    done = False
            if done:
                break

    @classmethod
    def start_elasticsearch_docker(cls):
        """Start the elasticsearch node via docker."""
        cls.docker_pull('elasticsearch:2.4')
        container_id = cls.cli.create_container(
            image='elasticsearch:2.4',
            ports=[9200],
            host_config=cls.cli.create_host_config(
                port_bindings={
                    9200: ('127.0.0.1', 9200)
                }
            )
        )
        cls.cli.start(container_id['Id'])
        cls.es_container_id = container_id['Id']

    @classmethod
    def start_postgres_docker(cls):
        """Start the postgres server via docker."""
        cls.docker_pull('postgres:latest')
        container_id = cls.cli.create_container(
            image='postgres:latest',
            ports=[5432],
            environment={
                'POSTGRES_PASSWORD': 'pacifica',
                'POSTGRES_DB': 'pacifica_metadata',
                'POSTGRES_USER': 'pacifica'
            },
            host_config=cls.cli.create_host_config(
                port_bindings={
                    5432: ('127.0.0.1', 5432)
                }
            )
        )
        cls.cli.start(container_id['Id'])
        cls.pg_container_id = container_id['Id']

    @classmethod
    def stop_elasticsearch_docker(cls):
        """Stop and blow away the elasticsearch docker container."""
        cls.cli.stop(cls.es_container_id)
        cls.cli.remove_container(cls.es_container_id)
        cls.es_container_id = None

    @classmethod
    def stop_postgres_docker(cls):
        """Stop and blow away the postgres docker container."""
        cls.cli.stop(cls.pg_container_id)
        cls.cli.remove_container(cls.pg_container_id)
        cls.pg_container_id = None

    @classmethod
    def setup_server(cls):
        """Start the cherrypy server."""
        logger = logging.getLogger('peewee')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())
        cls.start_postgres_docker()
        cls.start_elasticsearch_docker()
        create_tables()
        cherrypy.config.update('server.conf')
        cherrypy.tree.mount(Root(), '/', 'server.conf')

    @classmethod
    def teardown_class(cls):
        """Tear down the services required by the server."""
        super(TestCherryPyAPI, cls).teardown_class()
        cls.stop_elasticsearch_docker()
        cls.stop_postgres_docker()

    def test_methods(self):
        """Test the PUT (insert) method."""
        main()
        req = requests.get('{0}/keys?page_number=1&items_per_page=1'.format(self.url))
        self.assertEqual(req.status_code, 200)
        keys = loads(req.content)
        self.assertEqual(len(keys), 1)
        set_hash = {'key': 'Break Keys'}

        req = requests.post('{0}/keys'.format(self.url), data=dumps(set_hash), headers=self.headers)
        self.assertEqual(req.status_code, 200)
        req = requests.get('{0}/keys'.format(self.url))
        self.assertEqual(req.status_code, 200)
        keys = loads(req.content)
        self.assertEqual(len(keys), 2)
        for key in keys:
            self.assertEqual(key['key'], 'Break Keys')

        req = requests.get('{0}/keys'.format(self.url))
        self.assertEqual(req.status_code, 200)
        keys = loads(req.content)
        self.assertEqual(len(keys), 2)

        # update a forign key to something that isn't there
        req = requests.post('{0}/file_key_value?file_id=103'.format(self.url),
                            data='{"key_id": 107}', headers=self.headers)
        self.assertEqual(req.status_code, 500)
        req = requests.put('{0}/file_key_value'.format(self.url),
                           data='{"key_id": 107, "file_id": 103, "value_id": 103}',
                           headers=self.headers)
        self.assertEqual(req.status_code, 500)

        # just try invalid json
        req = requests.post('{0}/keys'.format(self.url), data='{ some bad json}', headers=self.headers)
        self.assertEqual(req.status_code, 500)
        req = requests.put('{0}/keys'.format(self.url), data='{ some bad json}', headers=self.headers)
        self.assertEqual(req.status_code, 500)

        # insert one item
        req = requests.put('{0}/keys'.format(self.url), data=dumps({'_id': 1, 'key': 'blarg'}), headers=self.headers)
        self.assertEqual(req.status_code, 200)

        # delete the item I just put in
        req = requests.delete('{0}/keys?key=blarg'.format(self.url))
        self.assertEqual(req.status_code, 200)

    def test_set_or_create(self):
        """Test the internal set or create method."""
        key = '{"_id": 4096, "key": "bigger"}'
        obj = Keys()
        # pylint: disable=protected-access
        obj._set_or_create(key)
        keys = '[{"_id": 4097, "key": "blah"}]'
        obj._set_or_create(keys)
        obj._set_or_create(key)
        hit_exception = False
        try:
            obj._set_or_create('{ bad json }')
        except cherrypy.HTTPError:
            hit_exception = True
        self.assertTrue(hit_exception)
        # pylint: enable=protected-access
