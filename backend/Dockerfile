# Production Dockerfile for Cronomarket Backend
FROM python:3.12-slim

# Prevent writing .pyc and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfiles and install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy

# Copy application files
COPY . /app/

# Port exposure
EXPOSE 8000

# Executing production server via gunicorn or standard manage runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
