#!/bin/bash
pylint --rcfile=pylintrc metadata
pylint --rcfile=pylintrc MetadataServer.py GenMetadataModelMD.py
radon cc metadata
