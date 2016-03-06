#!/bin/bash -xe

pylint metadata
python -m metadata.orm.test.base -v
python -m metadata.orm.test.keys -v
