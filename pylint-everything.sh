#!/bin/bash -xe

pylint --rcfile=pylintrc metadata
coverage run --include='metadata/*' pacifica-test.py -v
coverage report -m
