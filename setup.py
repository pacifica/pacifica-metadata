#!/usr/bin/python
"""Setup and install the metadata."""
from pip.req import parse_requirements
from setuptools import setup

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

setup(name='PacificaMetadata',
      version='1.0',
      description='Pacifica Metadata',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=['metadata'],
      scripts=['MetadataServer.py', 'DatabaseCreate.py'],
      install_requires=[str(ir.req) for ir in INSTALL_REQS])
