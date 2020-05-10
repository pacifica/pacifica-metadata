#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the metadata."""
from os import path
from setuptools import setup, find_packages


setup(
    name='pacifica-metadata',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica Metadata',
    url='https://github.com/pacifica/pacifica-metadata/',
    long_description=open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md')).read(),
    long_description_content_type='text/markdown',
    author='David Brown',
    author_email='dmlb2000@gmail.com',
    packages=find_packages(include=['pacifica.*']),
    namespace_packages=['pacifica'],
    entry_points={
        'console_scripts': [
            'pacifica-metadata=pacifica.metadata.__main__:main',
            'pacifica-metadata-cmd=pacifica.metadata.admin_cmd:main'
        ]
    },
    install_requires=[
        'cherrypy',
        'peewee>2',
        'psycopg2',
        'python-dateutil',
        'requests'
    ]
)
