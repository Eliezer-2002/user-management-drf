import django.db.models.deletion
from django.db import migrations, models


def migrate_ownership_and_roles(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    username_to_id = dict(User.objects.values_list("username", "id"))

    for user in User.objects.exclude(created_by__isnull=True).exclude(created_by=""):
        owner_id = username_to_id.get(user.created_by)
        if owner_id and owner_id != user.id:
            User.objects.filter(pk=user.pk).update(owner_id=owner_id)

    User.objects.filter(is_staff=True).update(is_manager=True)


def restore_string_ownership(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    owner_names = dict(User.objects.values_list("id", "username"))

    for user in User.objects.exclude(owner__isnull=True):
        User.objects.filter(pk=user.pk).update(
            created_by=owner_names.get(user.owner_id)
        )


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_manager",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether this user can manage subordinate users.",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                db_index=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="managed_users",
                to="accounts.user",
            ),
        ),
        migrations.RunPython(
            migrate_ownership_and_roles,
            reverse_code=restore_string_ownership,
        ),
        migrations.RemoveField(
            model_name="user",
            name="created_by",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="owner",
            new_name="created_by",
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["created_by", "id"], name="user_owner_id_idx"
            ),
        ),
    ]
