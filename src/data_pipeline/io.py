import csv
import hashlib
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from .models import Transaction

FIELDS = ["datetime_transaction", "iban_origine", "pays_source", "banque_source",
          "iban_destinataire", "pays_destinataire", "montant"]


def load_csv(path: str | Path) -> list[Transaction]:
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"Colonnes invalides dans {path.name}: {reader.fieldnames}")
        rows = []
        for row in reader:
            raw = ",".join(row[field] for field in FIELDS)
            tx_id = hashlib.sha256(raw.encode()).hexdigest()
            rows.append(Transaction(tx_id, datetime.fromisoformat(row["datetime_transaction"]),
                                    row["iban_origine"], row["pays_source"], row["banque_source"],
                                    row["iban_destinataire"], row["pays_destinataire"],
                                    Decimal(row["montant"])))
        return rows

