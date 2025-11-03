# Cumulus Geo Processors

Python package implementation to process incoming grids to Cloud Optimized GeoTIFF (COG).  The `Geoprocessor` is a Python module built into the package and referenced as a plugin using the `pyplugs` package.

## Basic Processor Requirements:

- The Python decorator `@pyplugs.register` defines the `process` method as the plugin
- The plugin name (python filename) has to match the Cumulus Acquirable name
  - Example: `nbm-co-01h` is the acquirable name and the processor name will be `nbm-co-01h.py`
- Processors have to reside under the directory `./src/cumulus_geoproc/processors`


## Processor Method

The following is the template for a `process` method in the geoprocessor module (acquirable.py file)

```python
@pyplugs.register
def process(*, src: str, dst: str = None, acquirable: str = None):
    """
    # Grid processor

    __Requires keyword only arguments (*)__

    Parameters
    ----------
    src : str
        path to input file for processing
    dst : str, optional
        path to temporary directory
    acquirable: str, optional
        acquirable slug

    Returns
    -------
    List[dict]
    ```
    {
        "filetype": str,         Matching database acquirable
        "file": str,             Converted file
        "datetime": str,         Valid Time, ISO format with timezone
        "version": str           Reference Time (forecast), ISO format with timezone
    }
    ```
    """
```

## Processor Returns

Processors always return a list of objects as defined below

```python
return [{
    "filetype": str,    Matching database acquirable
    "file": str,        Converted file
    "datetime": str,    Valid Time, ISO format with timezone
    "version": str      Reference Time (forecasts only), ISO format with timezone
}]
```

## Processor Local Development

This repository tries to provide two basic ways to develop and test processors, .devcontainer and docker-compose.  The `.devcontainer` uses the existing `docker-compose.yml` file and is used with VS Code.  The other method is executing `docker compose` at the command line with appropriate options and commands.  Either method will require the user to make sure the `docker-compose.yml` file settings are correct before execution. Make sure the `TEST_DATA_TAG: "2025-10-31"` targeting the geoproc-test-data is updated to the latest release.

There are three options in the `docker-compose.yml` file that should cover all needs during development. To run any of the options, uncomment the selected option in `docker-compose.yml` (but make sure the other two are commented out) and run `docker compose run --rm geoproc`. When you are finsihed run `docker compose down -v` to shutdown and remove the volume.

- Option 1: Run the container without it stopping and not run any processor
  - this options allows the user to "jump" into the container
- Option 2: Run `pytest` on all processors against the test data repo
  - use this option when finalizing processor and testing all before pushing for a Pull Request; a failed test will not allow merging
  - Note if the geoprocessor changes aren't included in the test, try to build the container with `docker compose build --no-cache geoproc` to make sure you are not testing with a cached geoprocessor.
- Option 3: Run the developing processor code defined in the `geoproc_develop/processor.py` file
  - Place the processor code you want to test in the `processor.py` file
  - Put a copy of the aquirable to be placed in the in the `geoproc_develop` directory
  - Update the argument following  `"/opt/geoproc/develop/runner.py"` in `the docker-compose.yml` with your aquirable name.  
    - example: `command: [ "/opt/geoproc/develop/runner.py", "abrfc_qpe_01hr_2025102413Z.nc.gz"]`

# Geoproc Test Data

Test data lives in the GitHub repository [USACE/cumulus-geoproc-test-data](https://github.com/USACE/cumulus-geoproc-test-data) as a release archive `tar.gz`. Each acquirable has its own directory with an example file(s) and `json` configuration file describing the test file(s). `pytest` `fixtures` is used to read each configuration `json` file, aggregate them into a single fixture, and uses them to define testing. There is a one-to-one releation between the processor and testing data.

The `tar.gz` also containes some helper scripts, `gen_markdown` and `tar_test_data.sh`. `gen_markdown` is a Python script creating `Markdown` from each `json` configuration creating [TESTDATA.md](./TESTDATA.md). The shell script `tar_test_data.sh` creates `cumulus-geoproc-test-data.tar.gz` if changes are added for a new release.

# **\*New release data requires a Docker file update**

```yaml
services:
  geoproc:
    build:
      context: .
      args:
        TEST_DATA_TAG: "2025-10-31"
```
To tag a geoproc-test-data release, in the geoproc-test-data repo use these commands:
`git tag -a 2025-10-15`
`git push origin 2023-09-15`