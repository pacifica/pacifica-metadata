#!/bin/bash -xe

pylint --rcfile=pylintrc metadata
python -m metadata.orm.test -v
