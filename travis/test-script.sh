#!/bin/bash -xe

if [ "$RUN_LINTS" = "true" ] ; then
  pre-commit run --all-files
elif [ "$RUN_DEPLOY" = "true" ] ; then
  bash -xe ./travis/test-deploy.sh
else
  bash -xe ./travis/static-analysis.sh
  bash -xe ./travis/unit-tests.sh
fi
