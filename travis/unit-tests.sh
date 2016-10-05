#!/bin/bash
coverage run --include='metadata/*' MetadataUnitTest.py -v
coverage report -m
codeclimate-test-reporter
