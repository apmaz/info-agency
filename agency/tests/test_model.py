from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from agency.models import Topic, Redactor, Newspaper


class ModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            name="Business",
        )
        self.redactor = get_user_model().objects.create_user(
            username="admin",
            first_name="Thomas",
            last_name="Dickens",
            password="password",
            years_of_experience=17,
        )
        self.newspaper = Newspaper.objects.create(
            title="Is IT still the best sphere to work?",
            content="Some text about Is IT still the best sphere to work.",
        )
        self.newspaper.publishers.add(self.redactor)
        self.newspaper.topic.add(self.topic)

    def test_topic_str(self):
        self.assertEqual(str(self.topic),f"{self.topic.name}"
        )

    def test_redactor_str_and_get_absolute_url(self):
        expected_url = reverse(
            "agency:redactor-detail", kwargs={"pk": self.redactor.pk}
        )
        self.assertEqual(self.redactor.get_absolute_url(), expected_url)
        self.assertEqual(
            str(self.redactor),
            f"{self.redactor.username} ({self.redactor.first_name} {self.redactor.last_name})"
        )

    def test_newspaper_str(self):
        self.assertEqual(str(self.newspaper), f"{self.newspaper.title}")

    def test_newspaper_have_topic_and_publishers(self):
        self.assertIn(self.redactor, self.newspaper.publishers.all())
        self.assertIn(self.topic, self.newspaper.topic.all())
