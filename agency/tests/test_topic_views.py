from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from agency.models import Topic


TOPIC_LIST_URL = reverse("agency:topic-list")


class PublicTopicTests(TestCase):
    def test_topic_login_required(self):
        response = self.client.get(TOPIC_LIST_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateTopicTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="password",
        )
        self.client.force_login(self.user)
        Topic.objects.create(name="Politics")
        Topic.objects.create(name="Country politics")
        Topic.objects.create(name="Crime")
        Topic.objects.create(name="Business")
        Topic.objects.create(name="Art")

    def test_topic_retrieve_list_view(self):
        response = self.client.get(TOPIC_LIST_URL)
        topics = Topic.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(topics),
            list(response.context["topic_list"])
        )
        self.assertTemplateUsed(response, "agency/topic_list.html")

    def test_search_form_in_topic(self):
        response = self.client.get(TOPIC_LIST_URL, {"name": "Politics"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Politics")
        self.assertContains(response, "Country politics")
        self.assertNotContains(response, "Crime")
        self.assertNotContains(response, "Business")
        self.assertNotContains(response, "Art")
