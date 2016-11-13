#!/bin/bash
coverage run --include='metadata/*' -m pytest -v
coverage report -m
codeclimate-test-reporter
