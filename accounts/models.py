from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_manager = models.BooleanField(
        default=False,
        help_text="Designates whether this user can manage subordinate users.",
    )
    created_by = models.ForeignKey(
        "self",
        blank=True,
        db_index=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="managed_users",
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        indexes = [models.Index(fields=["created_by", "id"], name="user_owner_id_idx")]
