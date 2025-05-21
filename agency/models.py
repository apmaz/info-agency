from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0, message="Value of experience should not be less than 0."),
            MaxValueValidator(80, message="Value of experience should not be more than 80."),
        ]
    )

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
        get_user_model(), related_name="newspapers_by_publisher"
    )

    def __str__(self):
        return self.title
