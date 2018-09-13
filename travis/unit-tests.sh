#!/bin/bash
export POSTGRES_ENV_POSTGRES_USER=postgres
export POSTGRES_ENV_POSTGRES_PASSWORD=
export NOTIFICATIONS_URL=http://127.0.0.1:8080
python test_files/cherrypy_catch.py &
coverage run --include='metadata/*' -m pytest -v metadata/orm metadata/elastic metadata/test
coverage run --include='metadata/*' -a -m pytest -v metadata/rest
coverage run --include='metadata/*' -a MetadataServer.py --stop-after-a-moment
coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
