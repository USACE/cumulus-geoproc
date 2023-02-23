#!/bin/bash

# set -x

case "$1" in
    itest)
        echo "Pytest"
        python3 -m pytest -v --html=/output/report.html --self-contained-html
        ;;
    *)
        echo "'$1' Not an option"
        ;;
esac
