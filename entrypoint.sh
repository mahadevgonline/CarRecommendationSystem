#!/bin/bash
# entrypoint.sh — Run migrations then start Gunicorn
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn..."
exec gunicorn OnlineCarRecommendationSystem.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 2 \
    --timeout 120
