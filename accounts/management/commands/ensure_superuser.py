import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import User


class Command(BaseCommand):
    help = "Create the environment-configured superuser when it does not exist"

    @transaction.atomic
    def handle(self, *args, **options):
        environment = {
            "username": os.environ.get("DJANGO_SUPERUSER_USERNAME"),
            "email": os.environ.get("DJANGO_SUPERUSER_EMAIL"),
            "password": os.environ.get("DJANGO_SUPERUSER_PASSWORD"),
        }
        missing = [name for name, value in environment.items() if not value]
        if missing:
            raise CommandError(
                "Missing superuser environment values: " + ", ".join(missing)
            )

        existing = User.objects.filter(username=environment["username"]).first()
        if existing:
            if not existing.is_superuser:
                raise CommandError(
                    "The configured username exists but is not a superuser."
                )
            self.stdout.write("Configured superuser already exists.")
            return

        User.objects.create_superuser(
            username=environment["username"],
            email=environment["email"],
            password=environment["password"],
            is_manager=True,
        )
        self.stdout.write(self.style.SUCCESS("Configured superuser created."))
