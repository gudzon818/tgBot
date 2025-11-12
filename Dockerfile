# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (optional):
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app
COPY . .

# Build-time metadata (injected by CI)
ARG APP_VERSION=dev
ARG GIT_SHA=unknown

# Runtime env (can be overridden at run time)
ENV LOG_LEVEL=INFO \
    LOG_FILE=/var/log/bot.log \
    APP_VERSION=${APP_VERSION} \
    GIT_SHA=${GIT_SHA}

# Expose app port (for webhook mode)
EXPOSE 8000

# Healthcheck (optional, lightweight)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD \
  python -c "import os,sys,http.client; h=os.environ.get('WEB_HOST','0.0.0.0'); p=int(os.environ.get('WEB_PORT','8000'));\nimport http.client as hc; c=hc.HTTPConnection(h,p,timeout=2);\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\ntry:\n c.request('GET','/health'); r=c.getresponse(); sys.exit(0 if r.status==200 else 1)\nexcept Exception:\n sys.exit(1)"

# Default command: run bot (polling or webhook handled inside app)
CMD ["python", "-m", "bot.app"]
