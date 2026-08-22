cd .ima/CANONICAL_AUTHORITY/ACTIVE
gunicorn app:app --bind 0.0.0.0:10000
