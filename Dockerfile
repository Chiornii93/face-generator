FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run_server.py .
COPY workflow.json .

CMD ["uvicorn", "run_server:app", "--host", "0.0.0.0", "--port", "8000"]
