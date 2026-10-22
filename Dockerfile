FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
COPY src ./src
RUN pip install --no-cache-dir .
CMD ["sh", "-c", "until python -m data_pipeline.s3_pipeline; do echo 'S3 pas encore disponible, retry dans 5s'; sleep 5; done"]
