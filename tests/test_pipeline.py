from decimal import Decimal

from data_pipeline.generate import generate_csv
from data_pipeline.io import load_csv
from data_pipeline.repository import connect, insert_file
from data_pipeline.transform import aggregate_transactions


def test_transform_is_correct_and_flags_large_transactions(tmp_path):
    path = generate_csv(tmp_path)
    transactions = load_csv(path)
    result = aggregate_transactions(transactions)
    assert result.sent_by_iban["FR7630006000011234567890189"] == Decimal("8150.00")
    assert result.sent_by_bank["BNP"] == Decimal("8150.00")
    assert result.received_by_iban["FR7630006000011234567890189"] == Decimal("11000.00")
    assert len(result.flagged_transaction_ids) == 3


def test_integration_inserts_once_and_retry_is_idempotent(tmp_path):
    path = generate_csv(tmp_path)
    txs = load_csv(path)
    db = connect(":memory:")
    aggregates = aggregate_transactions(txs)
    key = "fixture-file"
    assert insert_file(db, key, txs, aggregates) is True
    assert insert_file(db, key, txs, aggregates) is False
    assert db.execute("SELECT COUNT(*) FROM transactions").fetchone()[0] == 6
    assert db.execute("SELECT COUNT(*) FROM processed_files").fetchone()[0] == 1


def test_retry_retries_transient_insert_failure(tmp_path):
    path = generate_csv(tmp_path)
    txs = load_csv(path)
    db = connect(":memory:")
    aggregates = aggregate_transactions(txs)
    calls = {"count": 0}

    def flaky(db, key, txs, aggs):
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("simulated database outage")
        from data_pipeline.repository import _insert_once
        _insert_once(db, key, txs, aggs)

    assert insert_file(db, "retry-file", txs, aggregates, sleep_seconds=0, operation=flaky)
    assert calls["count"] == 2
