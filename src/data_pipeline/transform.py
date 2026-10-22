from collections import defaultdict
from collections.abc import Iterable
from decimal import Decimal

from .models import Aggregates, Transaction


def aggregate_transactions(transactions: Iterable[Transaction], threshold: Decimal = Decimal(5000)) -> Aggregates:
    """Transformation pure : aucune lecture/ecriture externe et aucune mutation d'entree."""
    sent_by_iban: dict[str, Decimal] = defaultdict(Decimal)
    sent_by_bank: dict[str, Decimal] = defaultdict(Decimal)
    received_by_iban: dict[str, Decimal] = defaultdict(Decimal)
    flagged: set[str] = set()

    for tx in transactions:
        sent_by_iban[tx.iban_origine] += tx.montant
        sent_by_bank[tx.banque_source] += tx.montant
        received_by_iban[tx.iban_destinataire] += tx.montant
        if tx.montant > threshold:
            flagged.add(tx.transaction_id)

    return Aggregates(dict(sent_by_iban), dict(sent_by_bank), dict(received_by_iban), frozenset(flagged))
