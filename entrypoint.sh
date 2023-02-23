#!/bin/bash

# set -x

if [ "$1" == "build" ]
then
    echo "Build testing container"
fi

python3 -m pytest -v --html=/tmp/report.html --self-contained-html

