"""Extraction légère de transactions depuis un texte brut.

Cette interface peut être remplacée par un SLM local sans modifier la pipeline.
"""

import re


def extract_transaction_fields(text: str) -> dict[str, str | None]:
    return {
        "iban_origine": _find(text, r"iban\s*(?:origine|source)\s*[:=]\s*([A-Z0-9]+)"),
        "iban_destinataire": _find(text, r"iban\s*(?:destinataire|destination)\s*[:=]\s*([A-Z0-9]+)"),
        "montant": _find(text, r"montant\s*[:=]\s*([0-9]+(?:[.,][0-9]{2})?)"),
    }


def _find(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).replace(",", ".") if match else None
