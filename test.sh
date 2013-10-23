#!/bin/bash
# Run emserver test suite
export DJANGO_SETTINGS_MODULE=emserver.settings
nosetests --nocapture
