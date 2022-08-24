#!/bin/bash

# set -x

# run the testing
# coverage run --source=. -m unittest "$*"
python3 -m pytest -v --html=/output/report.html --self-contained-html "$*"
# run the coverage report
# coverage report -m