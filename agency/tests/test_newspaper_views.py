from datetime import datetime, date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from agency.models import Topic, Newspaper, Redactor


NEWSPAPER_LIST_URL = reverse("agency:newspaper-list")


class PublicNewspaperTests(TestCase):
    def test_newspaper_login_required(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateNewspaperTests(TestCase):
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
            username="robo",
            first_name="Robert",
            last_name="Shakespeare",
            password="password",
            years_of_experience=7,
        )
        self.user_3 = get_user_model().objects.create_user(
            username="hardy",
            first_name="Arthur",
            last_name="Hardy",
            password="password",
            years_of_experience=17,
        )

        self.topic_1 = Topic.objects.create(name="Business")
        self.topic_2 = Topic.objects.create(name="Politics")
        self.topic_3 = Topic.objects.create(name="Technology")

        self.newspaper_1 = Newspaper.objects.create(
            title="Bitcoin Falls to the bottom!",
            content="Some text about Bitcoin Falls to the bottom!",
        )
        self.newspaper_1.topic.add(self.topic_1)
        self.newspaper_1.publishers.add(self.user_1)
        self.newspaper_1.published_date = "2025-04-15"
        self.newspaper_1.save(update_fields=["published_date"])

        self.newspaper_2 = Newspaper.objects.create(
            title="Using the command line in Linux",
            content="Some text about Using the command line in Linux",
        )
        self.newspaper_2.topic.add(self.topic_2)
        self.newspaper_2.publishers.add(self.user_2)
        self.newspaper_2.published_date = "2025-04-16"
        self.newspaper_2.save(update_fields=["published_date"])

        self.newspaper_3 = Newspaper.objects.create(
            title="What is the difference between Windows?",
            content="Some text about What is the difference between Windows?",
        )
        self.newspaper_3.topic.add(self.topic_3)
        self.newspaper_3.publishers.add(self.user_3)
        self.newspaper_3.published_date = "2025-04-17"
        self.newspaper_3.save(update_fields=["published_date"])

    def test_create_newspaper(self):
        form_data = {
            "title": "Is IT still the best sphere to work?",
            "content": "Some text about Is IT still the best sphere to work.",
            "topic": [self.topic_1.id],
            "publishers": [self.user_1.id],
        }
        self.client.post(reverse("agency:newspaper-create"), form_data)
        new_newspaper = Newspaper.objects.get(
            title=form_data["title"]
        )
        response = self.client.get(NEWSPAPER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            new_newspaper.title, form_data["title"]
        )

    def test_newspaper_retrieve_list_view(self):
        response = self.client.get(NEWSPAPER_LIST_URL)
        newspapers = Newspaper.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(newspapers),
            list(response.context["newspaper_list"])
        )
        self.assertTemplateUsed(response, "agency/newspaper_list.html")

    def test_search_form_with_title_filter_in_newspaper(self):
        response = self.client.get(
            NEWSPAPER_LIST_URL, {
                "query": "Bitcoin Falls to the bottom!",
                "search_by": "title"}
        )
        newspapers = response.context["newspaper_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Newspaper.objects.filter(
            title="Bitcoin Falls to the bottom!").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            title="Is IT still the best sphere to work?").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            title="What is the difference between Windows?").first(), newspapers
            )

    def test_search_form_with_content_filter_in_newspaper(self):
        response = self.client.get(
            NEWSPAPER_LIST_URL, {
                "query": "Some text about Bitcoin Falls to the bottom!",
                "search_by": "content"}
        )
        newspapers = response.context["newspaper_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Newspaper.objects.filter(
            content="Some text about Bitcoin Falls to the bottom!").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            content="Is IT still the best sphere to work?").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            content="What is the difference between Windows?").first(), newspapers
            )

    def test_search_form_with_published_date_filter_in_newspaper(self):
        response = self.client.get(
            NEWSPAPER_LIST_URL, {
                "query": "2025-04-17",
                "search_by": "published_date"}
        )
        newspapers = response.context["newspaper_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Newspaper.objects.filter(
            published_date="2025-04-17").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            published_date="2025-04-16").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            published_date="2025-04-15").first(), newspapers
            )

    def test_search_form_with_publishers_username_filter_in_newspaper(self):
        response = self.client.get(
            NEWSPAPER_LIST_URL, {
                "query": "admin",
                "search_by": "publishers_username"}
        )
        newspapers = response.context["newspaper_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Newspaper.objects.get(
            publishers__username="admin"), newspapers
        )
        self.assertNotIn(Newspaper.objects.get(
            publishers__username="robo"), newspapers
        )
        self.assertNotIn(Newspaper.objects.get(
            publishers__username="hardy"), newspapers
        )

    def test_search_form_with_publishers_first_name_filter_in_newspaper(self):
        response = self.client.get(
            NEWSPAPER_LIST_URL, {
                "query": "Thomas",
                "search_by": "publishers_first_name"}
        )
        newspapers = response.context["newspaper_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Newspaper.objects.filter(
            publishers__first_name="Thomas").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            publishers__first_name="Robert").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            publishers__first_name="Arthur").first(), newspapers
            )

    def test_search_form_with_publishers_last_name_filter_in_newspaper(self):
        response = self.client.get(
            NEWSPAPER_LIST_URL, {
                "query": "Dickens",
                "search_by": "publishers_last_name"}
        )
        newspapers = response.context["newspaper_list"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(Newspaper.objects.filter(
            publishers__last_name="Dickens").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            publishers__last_name="Shakespeare").first(), newspapers
            )
        self.assertNotIn(Newspaper.objects.filter(
            publishers__last_name="Hardy").first(), newspapers
            )

    def test_search_form_with_all_filter_in_newspapers(self):
        response = self.client.get(
            NEWSPAPER_LIST_URL, {"query": "Dickens", "search_by": "All Fields"}
        )
        newspapers = response.context["newspaper_list"]
        self.assertTrue(
            any(
                "Dickens" in newspaper.title or
                "Dickens" in newspaper.content or
                any(
                    "Dickens" in topic.name for topic in newspaper.topic.all()
                ) or
                "Dickens" in str(newspaper.published_date) or
                any(
                    "Dickens" in publishers.username for publishers in newspaper.publishers.all()
                ) or
                any(
                    "Dickens" in publishers.first_name for publishers in newspaper.publishers.all()
                ) or
                any(
                    "Dickens" in publishers.last_name for publishers in newspaper.publishers.all()
                )
                for newspaper in newspapers
            ),
        )
