"""Extraction OCR optionnelle pour des justificatifs de transactions."""

import re
from pathlib import Path


def extract_transaction_text(image_path: str | Path) -> str:
    """Utilise Tesseract si installé; l'import reste optionnel pour le chemin CSV."""
    import pytesseract
    from PIL import Image

    return pytesseract.image_to_string(Image.open(image_path))


def extract_amount(text: str) -> str | None:
    match = re.search(r"(?:montant|amount)\s*[:=]?\s*([0-9]+(?:[.,][0-9]{2})?)", text, re.IGNORECASE)
    return match.group(1).replace(",", ".") if match else None
