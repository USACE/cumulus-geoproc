# Geo Processors

Python package implementation to process incoming grids to Cloud Optimized GeoTIFF (COG)

## Geo Processor Development and Testing

### Development

...

### Testing

#### VS Code Developement Container

A VS Code development container configuration is provided to assist in processor and test development.  See [Create a Dev Container](https://code.visualstudio.com/docs/devcontainers/create-dev-container) to use a Docker container as a full-featured development environment.  A `devcontainer.json` configuration is provided already for development.

#### Testing the Processors

A shell script (`docker_run.sh`) is provided to build and run the docker container and run all tests.  The current shell script provides options to test (-t) and/or bind a volume to return a `Pytest` report (-k).  


