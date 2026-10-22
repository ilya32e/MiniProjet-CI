import os
import sqlite3

import streamlit as st

st.set_page_config(page_title="Transactions dashboard", layout="wide")
st.title("Financial data pipeline")
database = os.getenv("DATABASE", "pipeline.db")
db = sqlite3.connect(database)
transactions = db.execute("SELECT * FROM transactions ORDER BY datetime_transaction").fetchall()
aggregates = db.execute("SELECT dimension, dimension_key, total FROM aggregate_values").fetchall()
db.close()

col1, col2, col3 = st.columns(3)
col1.metric("Transactions", len(transactions))
col2.metric("Transactions flaggées", sum(row[-1] for row in transactions))
col3.metric("Fichiers traités", sqlite3.connect(database).execute("SELECT COUNT(*) FROM processed_files").fetchone()[0])
st.subheader("Agrégats")
st.dataframe(aggregates, use_container_width=True)
st.subheader("Transactions")
st.dataframe(transactions, use_container_width=True)
