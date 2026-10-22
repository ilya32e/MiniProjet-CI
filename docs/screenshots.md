# Preuves d'exécution

Les captures ont été réalisées après une exécution complète du projet.

## Dashboard

- URL : http://localhost:8501
- Résultat : 18 transactions, 3 fichiers traités et 9 transactions flaggées.

## Stockage S3 local

- Console RustFS : http://localhost:9011
- API S3 : http://localhost:9010
- Bucket utilisé : `transactions`
- Objets attendus : `incoming/transactions_001.csv`, `transactions_002.csv`, `transactions_003.csv`.

## CI/CD

- CI : https://github.com/ilya32e/MiniProjet-CI/actions/runs/39769720575
- CD Docker : https://github.com/ilya32e/MiniProjet-CI/actions/runs/39769720875

Les captures du dashboard, de la console RustFS et des workflows GitHub ont été effectuées pendant cette validation.
