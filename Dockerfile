FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir uvicorn && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "deadlock_assets_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
