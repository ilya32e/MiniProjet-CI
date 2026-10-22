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

## Retry, doublons et échec contrôlé

La démonstration reproductible est disponible avec :

```powershell
python scripts/demo_retry.py
```

Elle simule une panne pendant l'insertion, vérifie le retry, puis relance le
même fichier. La seconde exécution est ignorée grâce à la table
`processed_files`. Le test S3 vérifie aussi la nouvelle tentative après une
erreur temporaire de téléchargement.

- [Échec, retry et doublon](./screenshots/retry-duplicate.png)

## CI/CD

- CI : https://github.com/ilya32e/MiniProjet-CI/actions/runs/39770733042
- CD Docker : https://github.com/ilya32e/MiniProjet-CI/actions/runs/39770733011

Les captures du dashboard, de la console RustFS et des workflows GitHub ont été effectuées pendant cette validation.
