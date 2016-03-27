#!/bin/bash -xe

pylint --rcfile=pylintrc metadata
PYTHONPATH=$PWD python -m metadata.orm.test -v
