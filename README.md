# Geo Processors

Python package implementation to process incoming grids to Cloud Optimized GeoTIFF (COG)

### Iterative Development and Testing With Docker

The script `tests.sh` in the root of this repository copies the python code in `/src` into a docker container and runs all tests in the src/tests directory by default. The script supports the option `-k`, which will bind mount the directory cumulus-geoproc-test-results in this repository to the container directory `/output` at runtime. As a result, all output files from running unittest tests will be written to this directory and will be available for local manual evaluation and debugging.

By default, `./tests.sh` runs the full unittest test suite. However, it is helpful during iterative development of a new processors to limit the number of tests that are run for faster feedback. This can be done by uncommenting and modifying the last line of the `Dockerfile` and commenting-out the default CMD. The workflow of commenting/uncommenting lines in the Dockerfile may be improved in the future.

```
# Run all tests
CMD ["python3", "-m", "unittest", "discover", "-v", "tests"]

# Run a single test (helpful for developing new processors)
# CMD ["python3", "-m", "unittest", "-v", "tests/integration/test_one_thing.py"]
```
