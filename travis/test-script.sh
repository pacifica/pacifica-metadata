#!/bin/bash -xe

if [ "$RUN_LINTS" = "true" ] ; then
  pre-commit run --all-files
  bash -xe ./travis/static-analysis.sh
elif [ "$RUN_TESTS" = "true" ] ; then
  bash -xe ./travis/unit-tests.sh
else
  bash -xe ./travis/test-deploy.sh
fi
