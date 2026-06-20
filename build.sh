#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run outstanding migrations on your new Neon database
python manage.py migrate

# Collect static assets
python manage.py collectstatic --noinput
