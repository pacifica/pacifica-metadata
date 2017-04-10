#!/bin/bash
pylint --rcfile=pylintrc --disable=I metadata
pylint --rcfile=pylintrc --disable=I MetadataServer.py GenMetadataModelMD.py
radon cc metadata
