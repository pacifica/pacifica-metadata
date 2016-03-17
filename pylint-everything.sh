#!/bin/bash -xe

pylint metadata
python -m metadata.orm.test -v
