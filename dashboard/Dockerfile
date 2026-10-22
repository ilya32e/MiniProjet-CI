FROM python:3.12-slim
WORKDIR /dashboard
RUN pip install --no-cache-dir streamlit "psycopg[binary]>=3.1"
COPY app.py .
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
