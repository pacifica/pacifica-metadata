#!/bin/bash -xe

pylint --rcfile=pylintrc --extension-pkg-whitelist=pycurl metadata
coverage run --include='metadata/*' pacifica-test.py -v
coverage report -m
