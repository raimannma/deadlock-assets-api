FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python -m deadlock_assets_api.main
