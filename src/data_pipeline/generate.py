import csv
from pathlib import Path

FIELDS = ["datetime_transaction", "iban_origine", "pays_source", "banque_source",
          "iban_destinataire", "pays_destinataire", "montant"]
ROWS = [
    ["2026-01-01T09:00:00", "FR7630006000011234567890189", "FR", "BNP", "DE89370400440532013000", "DE", "1200.00"],
    ["2026-01-01T10:00:00", "FR7630006000011234567890189", "FR", "BNP", "ES9121000418450200051332", "ES", "6500.00"],
    ["2026-01-02T11:00:00", "DE89370400440532013000", "DE", "DB", "FR7630006000011234567890189", "FR", "3000.00"],
    ["2026-01-02T12:00:00", "ES9121000418450200051332", "ES", "Santander", "FR7630006000011234567890189", "FR", "8000.00"],
    ["2026-01-03T13:00:00", "FR7630006000011234567890189", "FR", "BNP", "DE89370400440532013000", "DE", "450.00"],
    ["2026-01-03T14:00:00", "DE89370400440532013000", "DE", "DB", "ES9121000418450200051332", "ES", "5100.00"],
]


def generate_csv(output_dir: str | Path, filename: str = "transactions_001.csv",
                 rows: list[list[str]] | None = None) -> Path:
    destination = Path(output_dir) / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDS)
        writer.writerows(rows or ROWS)
    return destination


def generate_multiple_csv(output_dir: str | Path, count: int = 3) -> list[Path]:
    """Génère plusieurs fichiers déterministes, chacun avec le même schéma métier."""
    files = []
    for index in range(1, count + 1):
        rows = [row.copy() for row in ROWS]
        for row_number, row in enumerate(rows):
            row[-1] = f"{float(row[-1]) + index * 100 + row_number:.2f}"
        files.append(generate_csv(output_dir, f"transactions_{index:03d}.csv", rows))
    return files


if __name__ == "__main__":
    print(generate_csv("data"))
