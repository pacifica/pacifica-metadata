#!/bin/bash -xe

pylint --rcfile=pylintrc --extension-pkg-whitelist=pycurl metadata
python -m metadata.orm.test -v
python -m metadata.elastic.test -v
