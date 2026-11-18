#!/bin/bash
# entrypoint.sh — Run migrations, seed initial data, then start Gunicorn
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Seeding initial cars, parts, and demo accounts..."
python populate_data.py || true

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn on port 8080..."
exec gunicorn OnlineCarRecommendationSystem.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 2 \
    --timeout 120
