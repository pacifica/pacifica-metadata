#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the metadata."""
from pip.req import parse_requirements
from setuptools import setup

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

setup(name='PacificaMetadata',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      description='Pacifica Metadata',
      author='David Brown',
      author_email='david.brown@pnnl.gov',
      packages=[
          'metadata',
          'metadata.elastic',
          'metadata.elastic.test',
          'metadata.orm',
          'metadata.orm.test',
          'metadata.rest',
          'metadata.rest.fileinfo_queries',
          'metadata.rest.instrument_queries',
          'metadata.rest.migration_queries',
          'metadata.rest.proposal_queries',
          'metadata.rest.reporting_queries',
          'metadata.rest.test',
          'metadata.rest.tkvinfo_queries',
          'metadata.rest.tkvupload_queries',
          'metadata.rest.transaction_queries',
          'metadata.rest.user_queries'
      ],
      scripts=['MetadataServer.py', 'DatabaseCreate.py'],
      entry_point={
          'console_scripts': ['MetadataServer=metadata:main']
      },
      install_requires=[str(ir.req) for ir in INSTALL_REQS])
