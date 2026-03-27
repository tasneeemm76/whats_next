ARG PYTHON_VERSION=3.11-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps needed by some Python packages (Postgres/client builds).
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -eux; \
    pip install --upgrade pip; \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /code

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Use PORT from Fly env if present, fallback to 8000.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 workshops.wsgi"]
