import os
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class EnsureSuperuserCommandTests(APITestCase):
    @patch.dict(
        os.environ,
        {
            "DJANGO_SUPERUSER_USERNAME": "deployer",
            "DJANGO_SUPERUSER_EMAIL": "deployer@example.com",
            "DJANGO_SUPERUSER_PASSWORD": "Deployment-passphrase-753!",
        },
    )
    def test_command_is_idempotent(self):
        output = StringIO()

        call_command("ensure_superuser", stdout=output)
        call_command("ensure_superuser", stdout=output)

        self.assertEqual(User.objects.filter(username="deployer").count(), 1)
        user = User.objects.get(username="deployer")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_manager)


class RegistrationTests(APITestCase):
    def test_registration_creates_manager_without_admin_access(self):
        response = self.client.post(
            reverse("register_user"),
            {
                "username": "newmanager",
                "email": "manager@example.com",
                "password": "A-strong-passphrase-394!",
                "confirm_password": "A-strong-passphrase-394!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="newmanager")
        self.assertTrue(user.is_manager)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password("A-strong-passphrase-394!"))

    def test_registration_rejects_weak_password(self):
        response = self.client.post(
            reverse("register_user"),
            {
                "username": "newmanager",
                "email": "manager@example.com",
                "password": "password",
                "confirm_password": "password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_manager_email_is_unique_case_insensitively(self):
        User.objects.create_user(
            username="existing",
            email="Manager@Example.com",
            password="A-strong-passphrase-394!",
            is_manager=True,
        )

        response = self.client.post(
            reverse("register_user"),
            {
                "username": "newmanager",
                "email": "manager@example.com",
                "password": "Another-strong-passphrase-572!",
                "confirm_password": "Another-strong-passphrase-572!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)


class UserApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manager = User.objects.create_user(
            username="manager_one",
            email="manager1@example.com",
            password="Manager-password-154!",
            is_manager=True,
        )
        cls.other_manager = User.objects.create_user(
            username="manager_two",
            email="manager2@example.com",
            password="Manager-password-286!",
            is_manager=True,
        )
        cls.owned_user = User.objects.create_user(
            username="owned_user",
            email="owned@example.com",
            password="Owned-password-154!",
            created_by=cls.manager,
        )
        cls.other_user = User.objects.create_user(
            username="other_user",
            email="other@example.com",
            password="Other-password-286!",
            created_by=cls.other_manager,
        )

    def setUp(self):
        self.client.force_authenticate(self.manager)

    def test_list_returns_only_users_owned_by_requesting_manager(self):
        response = self.client.get(reverse("user_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.owned_user.id)

    def test_manager_cannot_access_or_modify_another_managers_user(self):
        urls_and_methods = (
            (reverse("user_retrieve", args=[self.other_user.id]), self.client.get),
            (reverse("user_update", args=[self.other_user.id]), self.client.patch),
            (reverse("user_delete", args=[self.other_user.id]), self.client.delete),
        )

        for url, method in urls_and_methods:
            with self.subTest(url=url):
                response = method(
                    url,
                    {"username": "changed", "email": "changed@example.com"},
                    format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.username, "other_user")

    def test_create_assigns_owner_hashes_password_and_preserves_spaces(self):
        password = "  Complex-passphrase-419!  "
        response = self.client.post(
            reverse("user_create"),
            {
                "username": "created_user",
                "email": "created@example.com",
                "password": password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="created_user")
        self.assertEqual(user.created_by, self.manager)
        self.assertTrue(user.check_password(password))
        self.assertNotEqual(user.password, password)

    def test_create_requires_and_validates_password(self):
        missing = self.client.post(
            reverse("user_create"),
            {"username": "missing_password", "email": "missing@example.com"},
            format="json",
        )
        weak = self.client.post(
            reverse("user_create"),
            {
                "username": "weak_password",
                "email": "weak@example.com",
                "password": "password",
            },
            format="json",
        )

        self.assertEqual(missing.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(weak.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", missing.data)
        self.assertIn("password", weak.data)

    def test_non_manager_is_forbidden(self):
        self.client.force_authenticate(self.owned_user)
        response = self.client.get(reverse("user_list"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_routes_reject_methods_that_do_not_match_their_purpose(self):
        retrieve_delete = self.client.delete(
            reverse("user_retrieve", args=[self.owned_user.id])
        )
        delete_get = self.client.get(reverse("user_delete", args=[self.owned_user.id]))

        self.assertEqual(
            retrieve_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(delete_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_search_and_pagination_are_stable(self):
        for index in range(12):
            User.objects.create(
                username=f"person_{index:02d}",
                email=f"person{index:02d}@example.com",
                created_by=self.manager,
            )

        first_page = self.client.get(reverse("user_list"))
        second_page = self.client.get(reverse("user_list"), {"page": 2})
        search = self.client.get(reverse("user_list"), {"search": "person_05"})

        self.assertEqual(first_page.data["count"], 13)
        self.assertEqual(len(first_page.data["results"]), 12)
        self.assertEqual(len(second_page.data["results"]), 1)
        self.assertEqual(search.data["count"], 1)
        self.assertEqual(search.data["results"][0]["username"], "person_05")
