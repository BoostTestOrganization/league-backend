FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && \
    apt-get install -y curl

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app
COPY ./tests /tests
COPY ./scripts /scripts