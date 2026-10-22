import os

from .generate import generate_multiple_csv
from .pipeline import run_from_s3
from .s3_storage import S3Storage


def run() -> None:
    storage = S3Storage(
        os.getenv("S3_ENDPOINT", "http://minio:9000"),
        os.getenv("S3_ACCESS_KEY", "minio"),
        os.getenv("S3_SECRET_KEY", "minio123"),
        os.getenv("S3_BUCKET", "transactions"),
    )
    storage.ensure_bucket()
    files = generate_multiple_csv("/tmp/generated", count=3)
    for path in files:
        storage.upload(path, f"incoming/{path.name}")
    keys = [f"incoming/{path.name}" for path in files]
    run_from_s3(storage, keys, "/tmp/s3-cache", os.getenv("DATABASE", "pipeline.db"))
    print(f"Processed {len(keys)} CSV files from S3")


if __name__ == "__main__":
    run()
