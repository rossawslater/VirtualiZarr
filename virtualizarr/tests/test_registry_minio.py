import pytest
from obstore.store import MemoryStore

from virtualizarr.registry import ObjectStoreRegistry


def test_minio_path_style_resolve():
    """A registered `s3://bucket` should resolve against an http(s) path-style URL
    such as `http://minio:9000/bucket/path/to/object` and return the trailing path
    without duplicating the bucket."""

    registry = ObjectStoreRegistry()
    mem = MemoryStore()
    registry.register("s3://my-bucket", mem)

    url = "http://minio:9000/my-bucket/data/prefix/my-file.nc"
    ret, path = registry.resolve(url)

    assert ret is mem
    assert path == "data/prefix/my-file.nc"


def test_minio_path_style_root_bucket_only():
    """If the url points to the bucket root, resolve should return an empty path."""

    registry = ObjectStoreRegistry()
    mem = MemoryStore()
    registry.register("s3://my-bucket", mem)

    url = "http://minio:9000/my-bucket/"
    ret, path = registry.resolve(url)

    assert ret is mem
    assert path == ""


def test_http_host_with_bucket_in_path_prefer_s3_bucket():
    """When the hostname looks like an S3 host but the bucket is included in the
    path, prefer a registered `s3://<bucket>` entry so the returned path does
    not contain the bucket."""

    registry = ObjectStoreRegistry()
    mem = MemoryStore()
    registry.register("s3://gris-iv", mem)

    url = "http://sid-o.s3.jc.rl.ac.uk/gris-iv/mosaic/monthly/202411_mosaic.nc"
    ret, path = registry.resolve(url)

    assert ret is mem
    assert path == "mosaic/monthly/202411_mosaic.nc"
