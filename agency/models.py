from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from info_agency import settings


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def get_absolute_url(self):
        return reverse("agency:redactor-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topic = models.ManyToManyField(Topic, related_name="newspapers_by_topic")
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="newspapers_by_publisher"
    )

    def __str__(self):
        return self.title
