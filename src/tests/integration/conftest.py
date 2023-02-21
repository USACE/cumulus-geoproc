"""
Integration test methods to support testing
"""


import json
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
import requests

LOCAL_TEST_PRODUCTS = Path(Path(__file__).parent.joinpath("../../../")).resolve()
TEST_PRODUCTS = Path(__file__).parent.joinpath("fixtures/test_products.json").resolve()

OUTPUT_PRODUCTS = []


@pytest.fixture(scope="module")
def products(fqpn: Path = TEST_PRODUCTS) -> list:
    """products

    Parameters
    ----------
    fqpn : Path, optional
        path to json file, by default TEST_PRODUCTS

    Returns
    -------
    list
        list of objects defining a product
    """
    with fqpn.open("r", encoding="utf-8") as fpt:
        _products = json.loads(fpt.read())

    return _products


@pytest.fixture(scope="session")
def tiff_files(tmpdir_factory):
    """tiff_files

    Parameters
    ----------
    tmpdir_factory : TempdirFactory
        temp directory factor

    Returns
    -------
    py.path.local
        path object
    """
    return tmpdir_factory.mktemp("tiffs", numbered=True)


def request_product(
    url: str, name_pattern: str, date_time: datetime = datetime.utcnow()
) -> str:
    """request_product from provided url and save as a temporary file

    Parameters
    ----------
    url : str
        base url
    name_pattern : str
        filename datetime pattern
    date_time : datetime, optional
        datetime dependent part of the filename, by default datetime.utcnow()

    Returns
    -------
    str
        FQPN to temporary file
    """
    filename = date_time.strftime(name_pattern)

    sep = "/"
    if url.endswith("/"):
        sep = ""
    _url = "".join([url, sep, filename])

    with requests.get(_url, timeout=10, stream=True) as req:
        if req.status_code != 200:
            return "/tmp/file/does/not/exist"
        with NamedTemporaryFile(
            delete=False,
        ) as fpt:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    fpt.write(chunk)

    return fpt.name
