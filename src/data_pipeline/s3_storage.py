import time
from pathlib import Path

import boto3


class S3Storage:
    """Petit adaptateur compatible MinIO/S3 avec retry de lecture."""

    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, bucket: str):
        self.client = boto3.client("s3", endpoint_url=endpoint_url,
                                   aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.bucket = bucket

    def ensure_bucket(self) -> None:
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except self.client.exceptions.ClientError:
            self.client.create_bucket(Bucket=self.bucket)

    def upload(self, path: str | Path, key: str) -> None:
        self.client.upload_file(str(path), self.bucket, key)

    def download(self, key: str, destination: str | Path, attempts: int = 3) -> Path:
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(attempts):
            try:
                self.client.download_file(self.bucket, key, str(destination))
                return destination
            except Exception:
                if attempt == attempts - 1:
                    raise
                time.sleep(0.2 * (2 ** attempt))
        raise RuntimeError("Téléchargement S3 impossible")
