from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    created_by = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.username}             ({self.created_by})" if self.created_by else f"{self.username}"