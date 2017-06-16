#!/usr/bin/python
"""Setup and install the metadata."""
from setuptools import setup

setup(name='PacificaMetadata',
      version='1.0',
      description='Pacifica Metadata',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=['metadata'],
      scripts=['MetadataServer.py', 'DatabaseCreate.py'])
