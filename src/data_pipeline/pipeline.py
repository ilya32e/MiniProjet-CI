import hashlib
from pathlib import Path

from .io import load_csv
from .repository import connect, insert_file
from .transform import aggregate_transactions


def run(input_dir: str = "data", database: str = "pipeline.db") -> None:
    db = connect(database)
    for path in sorted(Path(input_dir).glob("*.csv")):
        file_key = hashlib.sha256(path.read_bytes()).hexdigest()
        transactions = load_csv(path)
        insert_file(db, file_key, transactions, aggregate_transactions(transactions))
    db.close()


def run_from_s3(storage, keys: list[str], work_dir: str = ".s3-cache", database: str = "pipeline.db") -> None:
    """Même pipeline, mais les CSV sont récupérés depuis le stockage S3/MinIO."""
    db = connect(database)
    for key in keys:
        local_path = storage.download(key, Path(work_dir) / Path(key).name)
        file_key = hashlib.sha256(local_path.read_bytes()).hexdigest()
        transactions = load_csv(local_path)
        insert_file(db, file_key, transactions, aggregate_transactions(transactions))
    db.close()


if __name__ == "__main__":
    run()
