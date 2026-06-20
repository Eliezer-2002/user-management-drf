#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run outstanding migrations
python manage.py migrate

# Collect static assets
python manage.py collectstatic --noinput

# Create superuser automatically using env variables
python manage.py createsuperuser --noinput || true
