#!/bin/bash
# Select current version of virtualenv:
VERSION=15.1.0
# Name your first "bootstrap" environment:
INITIAL_ENV=virtual_env
# Set to whatever python interpreter you want for your first environment:
PYTHON=$(which python)
#URL_BASE=https://pypi.python.org/packages/source/v/virtualenv
URL_BASE=https://pypi.python.org/packages/d4/0c/9840c08189e030873387a73b90ada981885010dd9aea134d6de30cd24cb8/virtualenv-15.1.0.tar.gz#md5=44e19f4134906fe2d75124427dc9b716

# --- Real work starts here ---
curl -o virtualenv-15.1.0.tar.gz $URL_BASE
tar xzf virtualenv-$VERSION.tar.gz
# Create the first "bootstrap" environment.
$PYTHON virtualenv-$VERSION/virtualenv.py $INITIAL_ENV
# Don't need this anymore.
rm -rf virtualenv-$VERSION
# Install virtualenv into the environment.
$INITIAL_ENV/bin/pip install virtualenv-$VERSION.tar.gz
source virtual_env/bin/activate
rm -rf virtualenv-$VERSION.tar.gz

