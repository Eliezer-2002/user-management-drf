# User Management System

A Django REST Framework application where registered manager accounts can create,
search, update, and delete only the users they own. The browser interface uses JWT
authentication and the API enforces ownership on every object lookup.

## Stack

- Python and Django
- Django REST Framework and Simple JWT
- SQLite for local development; PostgreSQL through `DATABASE_URL` in production
- Bootstrap, HTML, CSS, and JavaScript
- WhiteNoise and Gunicorn for deployment

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Local development falls back to `db.sqlite3`. Copy the values from `.env.example`
into your shell or hosting provider; this project does not automatically load `.env`
files.

Run validation with:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Roles

- **Manager:** may use the user-management API and can access only users linked to
  that manager through `created_by`.
- **Managed user:** has no user-management privileges.
- **Django staff/superuser:** reserved for Django admin access. A superuser can use
  the API as a manager, but API object access is still ownership-scoped.

Public registration creates a manager, not a Django staff user.

## API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| POST | `/api/newuserregister/` | Register a manager | Public |
| POST | `/api/token/` | Obtain access and refresh tokens | Public |
| POST | `/api/token/refresh/` | Refresh an access token | Public |
| GET | `/api/users/` | List/search owned users | Manager |
| POST | `/api/users/create/` | Create an owned user | Manager |
| GET | `/api/users/<id>/retrieve/` | Retrieve an owned user | Manager |
| PUT/PATCH | `/api/users/<id>/update/` | Update an owned user | Manager |
| DELETE | `/api/users/<id>/delete/` | Delete an owned user | Manager |

Search with `/api/users/?search=name` and paginate with `/api/users/?page=2`.
Send access tokens as `Authorization: Bearer <access-token>`.

## Seed data

Create a manager first, then run:

```bash
python manage.py seed_data --owner manager_username --count 50
```

Seeded accounts have unusable passwords unless `--password` is explicitly supplied.

## Production configuration

Required values:

- `DJANGO_SECRET_KEY`
- `DATABASE_URL`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

The deployment script installs dependencies, applies migrations, collects static
assets, and creates a superuser only when all three `DJANGO_SUPERUSER_*` values are
present. Configure the process command as:

```bash
gunicorn user_management.wsgi:application
```
