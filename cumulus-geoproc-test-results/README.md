# Cumulus-GeoProc Processor Testing

# Test Fixture: Pytest

[`pytest`](https://docs.pytest.org) is the Python testing tool used to test processors against their respective product files.  Results are compiled in a HTML report saved in this directory.  The tests are executed by the `docker_run.sh` shell script with arguments `-t`, `-b`, and/or `-k`.  It is recommended to allways build `(-b)` the docker image each run.  Testing is performed when `-t` is used and report output is kept with `-k`.
