# Financial data pipeline

Projet d'intégration continue : génération de CSV déterministes, transformations pures, insertion relationnelle idempotente et retries.

## Lancer localement

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m data_pipeline.generate
python -m data_pipeline.pipeline
pytest -q
```

La table `processed_files` garantit qu'un fichier déjà traité n'est pas retraité. Les transactions ont un identifiant SHA-256 déterministe et l'insertion est transactionnelle : une panne est rollbackée puis réessayée avec backoff exponentiel.

## Niveau 2

`docker compose up --build` démarre MinIO, génère trois CSV, les envoie dans le bucket `transactions`, les relit depuis S3 avec retry, puis les insère dans SQLite. Le dashboard Streamlit est disponible sur `http://localhost:8501`. L'adaptateur [s3_storage.py](./src/data_pipeline/s3_storage.py) utilise l'API S3 de MinIO avec retries et le traitement pur reste indépendant du stockage.

## Démonstration d'échec

Le test `test_retry_retries_transient_insert_failure` simule une panne de base au premier appel. La transaction est rollbackée, puis l'insertion réussit au deuxième essai. Pour les captures d'écran demandées, lancer `pytest -q -s` avec une erreur volontaire dans `flaky`, capturer l'échec dans le terminal, puis retirer l'erreur et capturer le retry réussi. La CI reproduit automatiquement ce contrôle.

Le CSV inclut `montant`, nécessaire aux règles métier, en plus des colonnes listées dans le sujet.
