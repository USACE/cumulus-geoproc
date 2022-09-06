FROM osgeo/gdal:ubuntu-full-3.5.0

ENV PYTHONUNBUFFERED=1
ENV PYTEST_ADDOPTS="--color=yes"

RUN apt-get update -y && apt-get install -y \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

# Install Pip Requirements
COPY ./requirements*.txt /
RUN pip3 install -r requirements-dev.txt

# Output File Location
RUN mkdir /output

# Source Code Directory
RUN mkdir /src
COPY src/ /src/

# Test Data
# TODO: Consider moving this to a location like "/cumulus-geoproc-test-data"
#       where it can be referenced with a fully-qualified-pathname
#       and can be cached as a docker build layer above copy of more frequently changing
#       source code in /src
COPY cumulus-geoproc-test-data/fixtures/ /src/tests/integration/fixtures/

COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /src

ENTRYPOINT [ "/entrypoint.sh" ]

# For Testing; Keep Container Running to shell inside
# ENTRYPOINT [ "/bin/sh", "-c", "while true; do sleep 2 && echo 'sleeping for 2 seconds'; done;" ]