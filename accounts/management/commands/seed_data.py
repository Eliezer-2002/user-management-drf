from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker

from accounts.models import User


class Command(BaseCommand):
    help = "Seed database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=50)
        parser.add_argument("--owner", help="Username of the manager who owns the data")
        parser.add_argument("--password", help="Optional password for all seeded users")

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["count"]
        if count < 1:
            raise CommandError("--count must be at least 1")

        managers = User.objects.filter(is_manager=True)
        owner = (
            managers.filter(username=options["owner"]).first()
            if options["owner"]
            else managers.first()
        )
        if owner is None:
            raise CommandError("Create a manager account before seeding users.")

        fake = Faker()
        for _ in range(count):
            user = User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                created_by=owner,
            )
            if options["password"]:
                user.set_password(options["password"])
            else:
                user.set_unusable_password()
            user.save()

        self.stdout.write(
            self.style.SUCCESS(f"Created {count} users for {owner.username}.")
        )
