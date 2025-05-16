from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestAdmin(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="superuser",
            password="password",
        )
        self.client.force_login(self.admin_user)

        self.redactor = get_user_model().objects.create_user(
            username="admin",
            first_name="Thomas",
            last_name="Dickens",
            password="password",
            years_of_experience = 15,
        )

    def test_redactor_years_of_experience_listed(self):
        url = reverse("admin:agency_redactor_changelist")
        response = self.client.get(url)
        self.assertContains(response, "years_of_experience")

    def test_redactor_detail_years_of_experience_listed(self):
        url = reverse(
            "admin:agency_redactor_change", args=[self.redactor.pk]
        )
        response = self.client.get(url)
        self.assertContains(response, "years_of_experience")

    def test_redactor_add_first_name_last_name_years_of_experience_listed(self):
        url = reverse("admin:agency_redactor_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "years_of_experience")
