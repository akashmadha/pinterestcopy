# Use official Python image
FROM python:3.11-slim

# set workdir
WORKDIR /app

# system deps (if needed, e.g. PostgreSQL client & build tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# copy requirements first for layer caching
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project
COPY . /app

# collectstatic (optional at build or run)
ENV PYTHONUNBUFFERED=1

# expose port
EXPOSE 8000

# Run migrations + collectstatic then start gunicorn by default (you can override)
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn Backend.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
