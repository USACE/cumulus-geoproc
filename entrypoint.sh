#!/bin/bash

# set -x

case "$1" in
    itest)
        echo "Pytest"
        python3 -m pytest -v --html=./docs/index.html --self-contained-html
        ;;
    *)
        echo "No option provided that can be used"
        ;;
esac
