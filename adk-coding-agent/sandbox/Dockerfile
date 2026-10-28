FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
        bash git zip unzip pandoc poppler-utils libreoffice-writer nodejs npm \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir python-docx defusedxml lxml pytest \
    && npm install -g docx

ENV NODE_PATH=/usr/local/lib/node_modules \
    PYTHONDONTWRITEBYTECODE=1
