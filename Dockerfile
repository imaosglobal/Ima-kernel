FROM python:3.12-slim

WORKDIR /ima

COPY . .

RUN pip install --no-cache-dir -r requirements.txt || true

EXPOSE 8080

CMD ["python","IMA_START.py"]
