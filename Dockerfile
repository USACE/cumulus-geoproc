FROM osgeo/gdal:ubuntu-full-3.5.0

ENV PYTHONUNBUFFERED=1
ENV PYTEST_ADDOPTS="--color=yes"

RUN apt-get update -y && apt-get install -y \
  python3-pip git \
  && rm -rf /var/lib/apt/lists/*

# Output File Location
RUN mkdir /output

# Source Code Directory
RUN mkdir /app

WORKDIR /app

COPY . /app/

# Install Pip Requirements
RUN pip3 install .
RUN pip3 install -r requirements-dev.txt

COPY ./entrypoint.sh /entrypoint.sh


# ENTRYPOINT [ "/entrypoint.sh" ]

# For Testing; Keep Container Running to shell inside
# ENTRYPOINT [ "/bin/sh", "-c", "while true; do sleep 2 && echo 'sleeping for 2 seconds'; done;" ]