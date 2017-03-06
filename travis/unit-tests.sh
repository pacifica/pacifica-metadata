#!/bin/bash
coverage run --include='metadata/*' -m pytest -v metadata/orm metadata/elastic metadata/test_client.py
coverage run --include='metadata/*' -a -m pytest -v metadata/rest
coverage report --show-missing --fail-under 100
if [[ $CODECLIMATE_REPO_TOKEN ]] ; then
  codeclimate-test-reporter
fi
