# NOTE: This dockerfile is only for testing and does not run in dev/test/prod.
# It is only run locally or in CI/CD workflows (Github)
# Versions should match the cumulus-api/async-geoproc/Dockerfile

FROM ghcr.io/osgeo/gdal:ubuntu-full-3.9.1

ENV PYTHONUNBUFFERED=1
ENV PYTEST_ADDOPTS="--color=yes"

# env var for test data version to use, which should always be the most up to date
ENV TEST_DATA_TAG=2023-11-08

RUN apt-get update -y \
  && apt-get install -y python3-pip curl \
  && rm -rf /var/lib/apt/lists/*

# Output File Location
RUN mkdir /output

# Source Code Directory
RUN mkdir /app

COPY . /app/

WORKDIR /app

# Get the test data before testing it
RUN curl -L https://github.com/USACE/cumulus-geoproc-test-data/releases/download/${TEST_DATA_TAG}/cumulus-geoproc-test-data.tar.gz \
  --output cumulus-geoproc-test-data.tar.gz && \
  tar -xzvf cumulus-geoproc-test-data.tar.gz && \
  rm -f cumulus-geoproc-test-data.tar.gz

# Install Pip Requirements
# This first install is the cumulus-geoproc package
RUN python3 -m venv /opt/myenv \
  && /opt/myenv/bin/pip install . \
  && /opt/myenv/bin/pip install -r requirements-dev.txt

# Prepend the virtual environment's bin directory to PATH
ENV PATH="/opt/myenv/bin:$PATH"

COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
