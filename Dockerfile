FROM ghcr.io/osgeo/gdal:ubuntu-full-3.9.1
ARG TEST_DATA_TAG

ENV PYTHONUNBUFFERED=1
ENV PYTEST_ADDOPTS="--color=yes"

ENV GEOPROC=/opt/geoproc
ENV GEOPROC_VENV=${GEOPROC}/venv

ENV PATH=${GEOPROC_VENV}/bin:$PATH

WORKDIR /opt/geoproc

# apt-get install -y python3-pip python3-venv
RUN apt-get -y update \
    && apt-get install python3.12-venv -y \
    && apt-get remove python3-pil -y

# Get the test data before testing it
ADD https://github.com/USACE/cumulus-geoproc-test-data/releases/download/${TEST_DATA_TAG}/cumulus-geoproc-test-data.tar.gz /opt/geoproc

RUN tar -xzvf cumulus-geoproc-test-data.tar.gz && \
    rm -f cumulus-geoproc-test-data.tar.gz

COPY docs/ mkdocs.yml requirements-dev.txt ./

COPY ./geoproc/ ./pkg

# install package in venv
RUN python3 -m venv --system-site-packages "$GEOPROC_VENV" \
    && . activate \
    && pip install -r requirements-dev.txt \
    && pip install -e ${GEOPROC}/pkg/

COPY --chmod=755 ./entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
