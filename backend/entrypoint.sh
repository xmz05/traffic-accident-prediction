#!/bin/sh

# Ждём, пока поднимется БД
echo "Waiting for PostgreSQL..."

while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started"

# Миграции
python manage.py migrate --noinput

# Статические файлы, если понадобятся
# python manage.py collectstatic --noinput

# Стартуем gunicorn
gunicorn traffic_risk.wsgi:application --bind 0.0.0.0:8000
