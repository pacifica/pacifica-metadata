#!/bin/bash
export NOTIFICATIONS_URL=http://127.0.0.1:8080
export PEEWEE_URL=postgres://postgres:@localhost/pacifica_metadata
python test_files/cherrypy_catch.py &
coverage run --include='pacifica/*' -m pytest -vx pacifica/metadata/orm pacifica/metadata/elastic pacifica/metadata/test
coverage run --include='pacifica/*' -a -m pytest -vx pacifica/metadata/rest
coverage run --include='pacifica/*' -a -m pacifica.metadata --stop-after-a-moment
coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
