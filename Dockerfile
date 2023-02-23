FROM osgeo/gdal:ubuntu-full-3.5.0

ENV PYTHONUNBUFFERED=1
ENV PYTEST_ADDOPTS="--color=yes"

ENV TEST_DATA_TAG=2023-02-22

RUN apt-get update -y && \
    apt-get install -y python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Output File Location
RUN mkdir /output

# Source Code Directory
RUN mkdir /app

COPY . /app/

WORKDIR /app/cumulus-geoproc

RUN curl -L https://github.com/USACE/cumulus-geoproc-test-data/releases/download/${TEST_DATA_TAG}/cumulus-geoproc-test-data.tar.gz \
    --output cumulus-geoproc-test-data.tar.gz && \
    tar -xzvf cumulus-geoproc-test-data.tar.gz


# Install Pip Requirements
# This first install is the cumulus-geoproc package
RUN pip3 install .
RUN pip3 install -r requirements-dev.txt

COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

CMD ["-b"]
