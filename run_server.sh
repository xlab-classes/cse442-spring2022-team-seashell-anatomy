#!/bin/bash

echo 'running tests...'

python -m unittest discover -v
RETVAL=$?

if [ $RETVAL -eq 0 ]
then
    echo 'running server...'
    export FLASK_APP=server.py
    flask run --host=0.0.0.0 -p $1
else
    echo 'tests failed, shutting down server...'
fi
