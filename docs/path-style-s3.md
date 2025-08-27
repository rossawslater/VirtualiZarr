# Path-style S3 (MinIO) support

VirtualiZarr's `ObjectStoreRegistry` supports resolving path-style S3 endpoints (commonly produced by MinIO or custom S3-compatible endpoints) to stores registered as `s3://<bucket>`.

Why this is needed

- MinIO and some custom S3 endpoints use path-style addressing: `http://minio:9000/<bucket>/path/to/object`.
- A normal S3 virtual-hosted URL looks like `https://<bucket>.s3.amazonaws.com/path/to/object` and the bucket is part of the hostname.

How VirtualiZarr handles this

- When resolving a URL, if an exact `(scheme, netloc)` key is not found and the URL looks like `http(s)://.../<bucket>/...`, the registry will try a fallback where it treats the first path segment as the bucket and match it against a registered `s3://<bucket>` store.
- The trailing path returned by `resolve()` will not include the bucket segment.

Recommendation

- When using MinIO or other path-style S3 endpoints, register your store with `s3://<bucket>` (for example `s3://my-bucket`) so the registry can match both `s3://...` URLs and path-style HTTP(S) URLs.

Examples

```py
from obstore.store import S3Store
from virtualizarr.registry import ObjectStoreRegistry

# Register as s3://<bucket>
s3store = S3Store(bucket="my-bucket")
reg = ObjectStoreRegistry()
reg.register("s3://my-bucket", s3store)

# These will both resolve to the same store:
reg.resolve("s3://my-bucket/path/to/file")
reg.resolve("http://minio:9000/my-bucket/path/to/file")
```
