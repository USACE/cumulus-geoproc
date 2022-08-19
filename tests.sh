#!/bin/bash

# Build Image
docker build -t cumulus-geoproc-tests:latest .

# -k option ('keep') bind-mounts ./cumulus-geoproc-test-results on host 
#                    to /output in container for manually evaluating output files
while getopts "k" option; do
    case ${option} in 
        k)
            VOLUMES="-v $PWD/cumulus-geoproc-test-results:/output"
    esac
done

docker run \
  ${VOLUMES} \
  -v $PWD/cumulus-geoproc-test-data/fixtures:/src/tests/integration/fixtures \
  cumulus-geoproc-tests:latest
