#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

# 1. Install required packages
pip install -r requirements.txt

# 2. Sync database structure
python manage.py migrate

# 3. Handle static assets
python manage.py collectstatic --noinput

# 4. This block gets skipped because your env variables are deleted (This is fine)
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_EMAIL:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
    python manage.py ensure_superuser
fi

# 5. TEMPORARY LINE: Replace "your_username_here" with your actual admin username
python manage.py seed_data --count 100 --owner "Eliezer" --password "TestPassword123!"
