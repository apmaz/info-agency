from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from agency.models import Redactor


REDACTOR_LIST_URL = reverse("agency:redactor-list")


class PublicRedactorTests(TestCase):
    def test_redactor_login_required(self):
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateRedactorTests(TestCase):
    def setUp(self):
        self.user_1 = get_user_model().objects.create_user(
            username="admin",
            first_name="Thomas",
            last_name="Dickens",
            password="password",
            years_of_experience = 15,
        )
        self.client.force_login(self.user_1)

        self.user_2 = get_user_model().objects.create_user(
            username="robert",
            first_name="Robert",
            last_name="Shakespeare",
            password="password",
            years_of_experience=7,
        )
        self.user_3 = get_user_model().objects.create_user(
            username="artur.hardy",
            first_name="Arthur",
            last_name="Hardy",
            password="password",
            years_of_experience=17,
        )
        self.user_4 = get_user_model().objects.create_user(
            username="john",
            first_name="John",
            last_name="James",
            password="password",
            years_of_experience=27,
        )

    def test_create_redactor(self):
        form_data = {
            "username": "username_0",
            "password1": "PasswordAPM17",
            "password2": "PasswordAPM17",
            "years_of_experience": 5,
        }
        self.client.post(reverse("agency:redactor-create"), form_data)
        response = self.client.get(REDACTOR_LIST_URL)

        new_redactor = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            new_redactor.years_of_experience, form_data["years_of_experience"]
        )

    def test_redactor_retrieve_list_view(self):
        response = self.client.get(REDACTOR_LIST_URL)
        redactors = Redactor.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(redactors),
            list(response.context["redactor_list"])
        )
        self.assertTemplateUsed(response, "agency/redactor_list.html")

    def test_search_form_with_username_filter_in_redactor(self):
        response = self.client.get(
            REDACTOR_LIST_URL, {"query": "robert", "search_by": "username"}
        )
        redactors = response.context["redactor_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Redactor.objects.get(username="robert"), redactors)
        self.assertNotIn(Redactor.objects.get(username="admin"), redactors)
        self.assertNotIn(Redactor.objects.get(username="artur.hardy"), redactors)
        self.assertNotIn(Redactor.objects.get(username="john"), redactors)

    def test_search_form_with_first_name_filter_in_redactor(self):
        response = self.client.get(
            REDACTOR_LIST_URL, {"query": "Arthur", "search_by": "first_name"}
        )
        redactors = response.context["redactor_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Redactor.objects.filter(first_name="Arthur").first(), redactors)
        self.assertNotIn(Redactor.objects.filter(first_name="Thomas").first(), redactors)
        self.assertNotIn(Redactor.objects.filter(first_name="Robert").first(), redactors)
        self.assertNotIn(Redactor.objects.filter(first_name="John").first(), redactors)

    def test_search_form_with_last_name_filter_in_redactor(self):
        response = self.client.get(
            REDACTOR_LIST_URL, {"query": "Hardy", "search_by": "last_name"}
        )
        redactors = response.context["redactor_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Redactor.objects.filter(last_name="Hardy").first(), redactors)
        self.assertNotIn(Redactor.objects.filter(last_name="Dickens").first(), redactors)
        self.assertNotIn(Redactor.objects.filter(last_name="Shakespeare").first(), redactors)
        self.assertNotIn(Redactor.objects.filter(last_name="James").first(), redactors)

    def test_search_form_with_years_of_experience_filter_in_redactor(self):
        response = self.client.get(
            REDACTOR_LIST_URL, {"query": "17", "search_by": "years_of_experience"}
        )
        redactors = response.context["redactor_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Redactor.objects.filter(years_of_experience=17).first(), redactors)
        self.assertNotIn(Redactor.objects.filter(years_of_experience=15).first(), redactors)
        self.assertNotIn(Redactor.objects.filter(years_of_experience=7).first(), redactors)
        self.assertNotIn(Redactor.objects.filter(years_of_experience=27).first(), redactors)

    def test_search_form_with_all_filter_in_redactor(self):
        response = self.client.get(
            REDACTOR_LIST_URL, {"query": "Arthur", "search_by": "All fields"}
        )
        redactors = response.context["redactor_list"]
        self.assertTrue(
            any(
                "Arthur" in redactor.username or
                "Arthur" in redactor.first_name or
                "Arthur" in redactor.last_name
                for redactor in redactors
            ),
        )
