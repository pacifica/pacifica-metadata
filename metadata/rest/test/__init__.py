#!/usr/bin/python
"""Test the REST interfaces."""
from json import loads
import logging
import cherrypy
from docker import Client
from metadata.orm import create_tables
from metadata.rest.root import Root


# pylint: disable=too-few-public-methods
class CPCommonTest(object):
    """Common test info for all rest."""

    PORT = 8121
    HOST = '127.0.0.1'
    url = 'http://{0}:{1}'.format(HOST, PORT)
    headers = {'content-type': 'application/json'}

    @staticmethod
    def setup_server():
        """Start the cherrypy server."""
        DockerMetadata.start_services()
# pylint: enable=too-few-public-methods


class DockerMetadata(object):
    """Docker wrapper to boot metadata backend services."""

    cli = Client()
    es_container_id = None
    pg_container_id = None

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
    def start_services(cls):
        """Start all the services."""
        logger = logging.getLogger('urllib2')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())
        cls.start_postgres_docker()
        cls.start_elasticsearch_docker()
        create_tables()
        cherrypy.config.update('server.conf')
        cherrypy.tree.mount(Root(), '/', 'server.conf')

    @classmethod
    def stop_services(cls):
        """Stop all the services."""
        cls.stop_elasticsearch_docker()
        cls.stop_postgres_docker()
