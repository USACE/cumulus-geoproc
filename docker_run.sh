#!/bin/bash


usage(){ printf "\n$0 usage:\n\n" && grep " .*)\ #" $0; exit 0;}

while getopts ":bhi" option; do
    case ${option} in 
        b) # Only build the container
            BUILD=true
            ;;
        i) # Run the integration test
            CMD="itest"
            echo "Setting 'CMD' to '${CMD}'"
            ;;
        k) # Attach a volume for reporting output
            VOLUMES="-v $PWD/cumulus-geoproc-test-results:/output"
            ;;
        h) # Print this message
            usage
            exit 1
            ;;
        *) # Print usage"
            usage
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
echo "docker run --rm ${VOLUMES} cumulus-geoproc-tests:latest ${CMD}"

# docker run --rm ${VOLUMES} cumulus-geoproc-tests:latest ${CMD}
