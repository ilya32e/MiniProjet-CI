from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    datetime_transaction: datetime
    iban_origine: str
    pays_source: str
    banque_source: str
    iban_destinataire: str
    pays_destinataire: str
    montant: Decimal


@dataclass(frozen=True)
class Aggregates:
    sent_by_iban: dict[str, Decimal]
    sent_by_bank: dict[str, Decimal]
    received_by_iban: dict[str, Decimal]
    flagged_transaction_ids: frozenset[str]

