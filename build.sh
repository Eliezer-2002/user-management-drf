#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --noinput

if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_EMAIL:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
    python manage.py ensure_superuser
fi
