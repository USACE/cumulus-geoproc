import hashlib
import json
import os
from pathlib import Path

cur_dir = Path(__file__).parent.absolute()


def remove_dot_properties():
    """remove_dot_properties"""
    for dirpath, _, filenames in os.walk(cur_dir / "cumulus-geoproc-test-data"):
        for filename in filenames:
            if filename.endswith(".properties"):
                Path(dirpath + "/" + filename).unlink(True)


def gen_json():
    """gen_json"""
    parent_dir = cur_dir.joinpath("cumulus-geoproc-test-data")
    test_products = []
    for dirpath, dirnames, filenames in os.walk(parent_dir):
        if len(dirnames) == 0:
            plugin = Path(dirpath).name
            if not plugin.startswith("wrf"):
                local_source = list(Path(dirpath).parts[2:])
                product = [p for p in filenames if not p.startswith(".")][0]
                local_source.append(product)
                local_source_path = "/".join(local_source)
                prod_obj = {
                    "plugin": plugin,
                    "url": "",
                    "local_source": local_source_path,
                    "vtype": "",
                    "name_pattern": product,
                }
                test_products.append(prod_obj)

    with open(
        "/workspaces/cumulus-geoproc/src/tests/integration/fixtures/test_products_testing.json",
        "w",
        encoding="utf-8",
    ) as fptr:
        fptr.write(json.dumps(test_products, indent=4))


def md5_hash():
    """md5_hash"""
    fixture_dir = (
        "/workspaces/cumulus-geoproc/cumulus-geoproc-test-data/fixtures/naefs-mean-06h"
    )
    hasher = hashlib.md5()
    all_dgst = []
    for dirpath, _, filenames in os.walk(fixture_dir):
        for file in filenames:
            with open(os.path.join(dirpath, file), "rb") as fptr:
                data = fptr.read()
                hasher.update(data)
                dgst = hasher.hexdigest()
                all_dgst.append(dgst)

    is_equal = len(all_dgst) == len(set(all_dgst))

    print(is_equal)


md5_hash()
