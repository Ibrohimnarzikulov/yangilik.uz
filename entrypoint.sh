#!/bin/sh
set -e

echo "==> Migratsiya..."
python manage.py migrate --noinput

echo "==> Tarjimalar..."
python manage.py compilemessages 2>/dev/null || echo "(compilemessages o'tkazildi)"

echo "==> Static yig'ish..."
python manage.py collectstatic --noinput --clear

echo "==> Ishga tushmoqda..."
exec "$@"