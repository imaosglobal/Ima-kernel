FROM python:3.12-slim

WORKDIR /ima

COPY . .

# CACHE_BUST 391492f

RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; else echo 'No requirements.txt found - skipping'; fi

EXPOSE 8080

CMD ["python3","production_server.py"]
