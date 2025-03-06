#!/bin/bash


usage(){ printf "\n$0 usage:\n\n" && grep " .*)\ #" $0; printf "\nexample: ./docker_run.sh -tb -a "TEST_DATA_TAG=2025-01-31"\n"; exit 0;}

BUILD=false
BUILD_ARG=""

while getopts ":a:bhkt" option; do
    case ${option} in 
        a) # adding an argument to the docker build
            BUILD_ARG="--build-arg ${OPTARG}"
            ;;
        b) # Build the docker image
            BUILD=true
            ;;
        t) # Run the integration test
            CMD="itest"
            echo "Setting 'CMD' to '${CMD}'"
            ;;
        k) # Attach a volume for reporting output
            VOLUMES="-v $PWD/cumulus-geoproc-test-results:/tmp/pytest-of-root/pytest-current/tiffscurrent"
            echo "Adding a volume: ${VOLUMES}"
            ;;
        h) # Print this message
            usage
            exit 1
            ;;
        *) # Print this message
            usage
            exit 1
            ;;
    esac
done

# Build Image
if [ "$BUILD" == "true" ]
then
    echo "docker build ${BUILD_ARG} -t cumulus-geoproc-tests:latest ."
    docker build ${BUILD_ARG} -t cumulus-geoproc-tests:latest .
fi

# Run container
docker run \
    --rm ${VOLUMES} \
    cumulus-geoproc-tests:latest ${CMD}
