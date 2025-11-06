#!/bin/bash

# Wait for postgres to be ready
until pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USERNAME; do
  echo "Waiting for postgres..."
  sleep 2
done

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start server
exec "$@"
