FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We won't copy code here for dev; we mount it via volumes
EXPOSE 8000

CMD ["uvicorn", "src.index:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
