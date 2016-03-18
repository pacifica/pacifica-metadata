#!/bin/bash -xe

pylint metadata
PYTHONPATH=$PWD python -m metadata.orm.test -v
