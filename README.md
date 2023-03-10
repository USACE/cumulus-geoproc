# Cumulus Geo Processors

Python package implementation to process incoming grids to Cloud Optimized GeoTIFF (COG)

# Geo Processor Development

## Basic Processor Requirements:

- Python modules using `pyplugs` to register the processor as a Python plugin
  - decorator `@pyplugs.register` defines method as the plugin
- Python file name matches Cumulus Acquirable name
  - `nbm-co-01h` --> `nbm-co-01h.py`
- Lives in `./src/cumulus_geoproc/processors`
- Method arguments are:
    ```
    src : str
        path to input file for processing
    dst : str, optional
        path to temporary directory
    acquirable: str, optional
        acquirable slug
    ```

- Must return list of objects (dictionary)
    ```
    [{
        "filetype": str,    Matching database acquirable
        "file": str,        Converted file
        "datetime": str,    Valid Time, ISO format with timezone
        "version": str      Reference Time (forecasts only), ISO format with timezone
    }]
    ```

## Unit and Integration Tests

The `pytest` framework was selected to test processors due to its ease in writing simple tests, readability and scalability.  The `tests` directory is under the `./src` directory next to the `cumulus_geoproc` package.  Test data for each processor lives in the GitHub repository [USACE/cumulus-geoproc-test-data](https://github.com/USACE/cumulus-geoproc-test-data).  There are many ways to run these tests but two options are configured here, Docker Container and VS Code Development Environment.  The VS Code Dev Env uses the `Dockerfile` to configure the container.

### Testing on the Comman Line

A shell script, `docker_run.sh`, is provided to build and test the processors.  Options `-t` and `-k` run the tests and create a volume returning a report of the tests.  If the docker image has not been created, or it needs a rebuild, the `-b` option must be provided.

Build and test without report generation:
```
> ./docker_run.sh -bt
```

Build and test with report generation:
```
> ./docker_run.sh -btk
```

## VS Code Developement Container

A VS Code development container configuration is provided to assist in processor and test development.  See [Create a Dev Container](https://code.visualstudio.com/docs/devcontainers/create-dev-container) to use a Docker container as a full-featured development environment.  A `devcontainer.json` configuration is provided already for development.

# Processor Test Data

Test data lives in the GitHub repository [USACE/cumulus-geoproc-test-data](https://github.com/USACE/cumulus-geoproc-test-data) as a release archive `tar.gz`.  Each acquirable has its own directory with an example file(s) and `json` configuration file describing the test file(s).  `pytest` `fixtures` is used to read each configuration `json` file, aggregate them into a single fixture, and uses them to define testing.  There is a one-to-one releation between the processor and testing data.

The `tar.gz` also containes some helper scripts, `gen_markdown` and `tar_test_data.sh`.  `gen_markdown` is a Python script creating `Markdown` from each `json` configuration creating [TESTDATA.md](./TESTDATA.md).  The shell script `tar_test_data.sh` creates `cumulus-geoproc-test-data.tar.gz` if changes are added for a new release.

***New release data requires the Docker file update `ENV TEST_DATA_TAG=YYYY-MM-DD`**
