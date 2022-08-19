FROM osgeo/gdal:ubuntu-small-3.5.0

ENV PYTHONUNBUFFERED=1

RUN apt-get update -y && apt-get install -y \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

# Install Pip Requirements
#   -- TODO: Probably a cleaner way to do this rather
#   --       than duplicating setup.cfg's install_requires
RUN pip3 install \
    httpx \
    httpx[http2] \
    boto3==1.21.29 \
    botocore==1.24.29 \
    numpy==1.22.3 \
    celery==5.2.3 \
    pyplugs==0.4.0 \
    netCDF4==1.5.8 \
    requests==2.27.1 \
    GDAL==3.4.2 \
    gdal-utils==3.4.1.0 \
    psycopg2-binary==2.9.3

# Output File Location
RUN mkdir /output

# Source Code Directory
RUN mkdir /src
COPY src/ /src/
WORKDIR /src

# Run all tests
CMD ["python3", "-m", "unittest", "discover", "-v", "tests"]

# Run a single test (helpful for developing new processors)
# CMD ["python3", "-m", "unittest", "-v", "tests/integration/hrrr-total-precip/test_hrrr_total_precip_20220818_f06.py"]
