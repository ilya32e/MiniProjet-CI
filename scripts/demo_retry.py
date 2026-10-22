"""Demonstration reproductible du retry et de l'idempotence."""

from data_pipeline.generate import generate_csv
from data_pipeline.io import load_csv
from data_pipeline.repository import _insert_once, connect, insert_file
from data_pipeline.transform import aggregate_transactions


def main() -> None:
    path = generate_csv("tmp-check")
    transactions = load_csv(path)
    aggregates = aggregate_transactions(transactions)
    db = connect(":memory:")
    calls = {"count": 0}

    def flaky_operation(connection, file_key, txs, result):
        calls["count"] += 1
        if calls["count"] == 1:
            print("[1/3] INSERTION: panne PostgreSQL simulee")
            raise RuntimeError("simulated database outage")
        print("[2/3] RETRY: insertion relancee avec succes")
        _insert_once(connection, file_key, txs, result)

    inserted = insert_file(db, "demo-retry.csv", transactions, aggregates,
                           sleep_seconds=0, operation=flaky_operation)
    duplicate = insert_file(db, "demo-retry.csv", transactions, aggregates,
                            sleep_seconds=0)
    transaction_count = db.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    processed_count = db.execute("SELECT COUNT(*) FROM processed_files").fetchone()[0]
    print(f"[3/3] DOUBLON: fichier ignore = {not duplicate}")
    print(f"resultat: inserted={inserted}, transactions={transaction_count}, "
          f"fichiers_traites={processed_count}, appels_insertion={calls['count']}")


if __name__ == "__main__":
    main()
