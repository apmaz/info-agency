from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from agency.models import Topic, Redactor, Newspaper


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    search_fields = ("username", "first_name", "last_name",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                    )
                },
            ),
        )
    )


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("title", "published_date")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)
