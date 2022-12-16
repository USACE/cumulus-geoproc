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

COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /src

ENTRYPOINT [ "/entrypoint.sh" ]

# For Testing; Keep Container Running to shell inside
# ENTRYPOINT [ "/bin/sh", "-c", "while true; do sleep 2 && echo 'sleeping for 2 seconds'; done;" ]