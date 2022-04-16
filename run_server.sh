#!/bin/bash

echo 'running tests...'

python -m unittest discover -v
echo "hello world"
RETVAL=$?

if [ $RETVAL -ne 0 ]
then
    echo 'tests failed, shutting down server...'
    exit 1
fi

echo 'running server...'
export FLASK_APP=server.py

if [ $# -eq 0 ]
then
    flask run --host=0.0.0.0 -p 8000
elif [ $# -eq 1 ]
then
    flask run --host=0.0.0.0 -p $1
else
    echo 'invalid number of arguments'
    exit 1
fi

