FROM python:3.10.0a1-alpine3.12

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=reservations.settings.local

COPY requirements.txt /app/requirements.txt

# Configure server
RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# working directory \
WORKDIR /app

ADD . .
