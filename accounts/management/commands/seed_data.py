from django.core.management.base import BaseCommand
from accounts.models import User
from faker import Faker

class Command(BaseCommand):

    help = "Seed database with fake data"

    def handle(self, *args, **options):

        fake = Faker()
        
        for _ in range(50):
            User.objects.create_user(
                username = fake.user_name(),
                email = fake.email(),
                password = "#demo123",
                # created_by = "your_user_name"
            )
        
        self.stdout.write(self.style.SUCCESS("Fake data created"))