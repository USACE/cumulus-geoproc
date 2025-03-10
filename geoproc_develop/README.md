# Geo Process Development

The `geoproc_develop` directory is setup to run and develop a processor with an example product file.

Setup:

- Add example product file
- The docker-compose.yml file has the `entrypoint` set as:
  - `entrypoint: ["python3"]`
-  The docker-compose.yml file has the `command` set as:
   -  `command: [ "/opt/geoproc/develop/runner.py", "example_filename"]`
   -  replace "example_filename" with actual filename

Volume Setup:

- `./geoproc_develop:/opt/geoproc/develop:rw`
- Sets the scripts in the container at /opt/geoproc/develop
- Output file result saved on host machine

Run:

- At the command line `docker compose up --build`
