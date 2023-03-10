#!/bin/bash


usage(){ printf "\n$0 usage:\n\n" && grep " .*)\ #" $0; exit 0;}

BUILD=false

while getopts ":bhkt" option; do
    case ${option} in 
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
    echo "docker build -t cumulus-geoproc-tests:latest ."
    docker build -t cumulus-geoproc-tests:latest .
fi

# Run container
docker run \
    --rm ${VOLUMES} \
    cumulus-geoproc-tests:latest ${CMD}
