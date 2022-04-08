#!/bin/bash

if [ -z $VIRTUAL_ENV ]
then
    echo 'activating venv...'
    source venv/bin/activate
fi

echo 'running tests...'

python -m unittest discover -v
RETVAL=$?

if [ $RETVAL -ne 0 ]
then
    echo 'tests failed, shutting down server...'
    exit 0
fi

echo 'running server...'
export FLASK_APP=server.py
flask run --host=0.0.0.0 -p $1

