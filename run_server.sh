#!/bin/bash

if [ -z $VIRTUAL_ENV ]
then
    echo 'activating venv...'
    source venv/bin/activate
fi

'
if [ ! -d 'dart-sass' ]
then
    echo 'installing sass...'
    wget 'https://github.com/sass/dart-sass/releases/download/1.49.10/dart-sass-1.49.10-linux-x64.tar.gz'
fi

echo 'adding Sass to PATH'
SASS=$(dirname "$BASH_SOURCE")/dart-sass
export PATH=$SASS:$PATH
'

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

