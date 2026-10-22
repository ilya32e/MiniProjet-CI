import sqlite3
import time
from collections.abc import Callable

from .models import Aggregates, Transaction

SCHEMA = """
CREATE TABLE IF NOT EXISTS processed_files (file_key TEXT PRIMARY KEY, processed_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS transactions (transaction_id TEXT PRIMARY KEY, file_key TEXT NOT NULL,
  datetime_transaction TEXT NOT NULL, iban_origine TEXT NOT NULL, pays_source TEXT NOT NULL,
  banque_source TEXT NOT NULL, iban_destinataire TEXT NOT NULL, pays_destinataire TEXT NOT NULL,
  montant NUMERIC NOT NULL, flagged INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS aggregate_values (dimension TEXT NOT NULL, dimension_key TEXT NOT NULL,
  total NUMERIC NOT NULL, PRIMARY KEY (dimension, dimension_key));
"""


def connect(database: str = "pipeline.db") -> sqlite3.Connection:
    db = sqlite3.connect(database)
    db.executescript(SCHEMA)
    return db


def insert_file(db: sqlite3.Connection, file_key: str, transactions: list[Transaction], aggregates: Aggregates,
                attempts: int = 3, sleep_seconds: float = 0.2,
                operation: Callable | None = None) -> bool:
    """Insertion idempotente. Le meme file_key ne sera jamais insere deux fois, meme apres retry."""
    operation = operation or _insert_once
    for attempt in range(attempts):
        try:
            if db.execute("SELECT 1 FROM processed_files WHERE file_key=?", (file_key,)).fetchone():
                return False
            operation(db, file_key, transactions, aggregates)
            db.commit()
            return True
        except Exception:
            db.rollback()
            if attempt == attempts - 1:
                raise
            time.sleep(sleep_seconds * (2 ** attempt))
    return False


def _insert_once(db, file_key, transactions, aggregates):
    for tx in transactions:
        db.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?)",
                   (tx.transaction_id, file_key, tx.datetime_transaction.isoformat(), tx.iban_origine,
                    tx.pays_source, tx.banque_source, tx.iban_destinataire, tx.pays_destinataire,
                    str(tx.montant), int(tx.transaction_id in aggregates.flagged_transaction_ids)))
    for dimension, values in (("sent_by_iban", aggregates.sent_by_iban),
                              ("sent_by_bank", aggregates.sent_by_bank),
                              ("received_by_iban", aggregates.received_by_iban)):
        for key, total in values.items():
            db.execute(
                """INSERT INTO aggregate_values VALUES (?,?,?)
                   ON CONFLICT(dimension, dimension_key)
                   DO UPDATE SET total = aggregate_values.total + excluded.total""",
                (dimension, key, str(total)),
            )
    db.execute("INSERT INTO processed_files VALUES (?, datetime('now'))", (file_key,))
