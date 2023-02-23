#!/bin/bash


usage(){ printf "\n$0 usage:\n\n" && grep " .*)\ #" $0; exit 0;}

while getopts ":bh" option; do
    case ${option} in 
        b) #
            CMD="build"
            ;;
        h) # Print this message
            usage
            exit 1
            ;;
    esac
done

# Build Image
docker build -t cumulus-geoproc-tests:latest .

docker run --rm cumulus-geoproc-tests:latest $CMD
