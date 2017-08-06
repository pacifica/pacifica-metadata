#!/bin/bash

uwsgi \
  --http-socket 0.0.0.0:8121 \
  --master \
  --die-on-term \
  --wsgi-file /usr/src/app/MetadataServer.py "$@"
