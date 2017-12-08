#!/bin/bash
export POSTGRES_ENV_POSTGRES_USER=postgres
export POSTGRES_ENV_POSTGRES_PASSWORD=
coverage run --include='metadata/*' -m pytest -v metadata/orm metadata/elastic metadata/test_client.py
coverage run --include='metadata/*' -a -m pytest -v metadata/rest
coverage run --include='metadata/*' -a MetadataServer.py &
SERVER_PID=$!
sleep 4
kill $SERVER_PID
sleep 4
coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
