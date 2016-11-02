#!/bin/bash
coverage run --include='metadata/*' -m unittest discover -v
coverage report -m
codeclimate-test-reporter
