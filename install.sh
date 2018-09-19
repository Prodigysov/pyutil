#!/bin/bash

if [[ "$(python --version 2>&1)" == "Python 3"* ]]; then
        pip install --upgrade git+git://github.com/prodigysov/pyutil.git
else
        echo "Requires Python 3!" 1>&2
fi
