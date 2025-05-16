from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.safestring import mark_safe

from agency.models import Redactor, Newspaper, Topic


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["placeholder"] = "Enter username"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm password"
        self.fields["first_name"].widget.attrs["placeholder"] = "First name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last name"

        self.fields["username"].widget.attrs["style"] = "color: white;"
        self.fields["password1"].widget.attrs["style"] = "color: white;"
        self.fields["password2"].widget.attrs["style"] = "color: white;"
        self.fields["first_name"].widget.attrs["style"] = "color: white;"
        self.fields["last_name"].widget.attrs["style"] = "color: white;"


class RedactorExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ("years_of_experience",)


class NewspaperCustomForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ("title", "content", "topic", "publishers",)

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
        "placeholder": "Enter title",
                       "style": "color: white;",
            }
        ),

        label=mark_safe("<strong>Title</strong>"),
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
            "rows": 5,
            "cols": 20,
            "placeholder": "Enter content",
                "style": "color: white;",
            }
        ),
        label=mark_safe("<strong>Content</strong>"),
    )

    topic = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=mark_safe("<strong>Choose a topic</strong>")
    )

    publishers = forms.ModelMultipleChoiceField(
        queryset=Redactor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label=mark_safe("<strong>Choose a redactor</strong>")
    )


class TopicCustomForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ("name",)

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter topic name",
                "style": "color: white;"
            }
        )
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name",
                "style": "width: 200px;",
            }
        ),
    )


class RedactorSearchForm(forms.Form):
    SEARCH_CHOICES = [
        ("username", "Username"),
        ("first_name", "First name"),
        ("last_name", "Last name"),
        ("years_of_experience", "Years of experience"),
        ("all", "All fields"),
    ]

    query = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "color: white; background-color: transparent; border-color: white; width: 150px;",
                "placeholder": "Search with filter...",
            }
        ),
    )

    search_by = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        label="",
        required=False,
        widget=forms.Select(
            attrs={
                "style": "color: white; width: 150px;"
            }
        )
    )



class NewspaperSearchForm(forms.Form):
    SEARCH_CHOICES = [
        ("title", "Title"),
        ("content", "Content"),
        ("topic", "Topic"),
        ("published_date", "Published date (YYYY-MM-DD)"),
        ("publishers_username", "Publisher (Username)"),
        ("publishers_first_name", "Publisher (First name)"),
        ("publishers_last_name", "Publisher (Last name)"),
        ("all", "All Fields"),
    ]

    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "color: white; background-color: transparent; border-color: white; width: 150px;",
                "placeholder": "Search with filter...",
            }
        ),
    )

    search_by = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        required=False,
        label="",
        widget=forms.Select(
            attrs={
                "style": "color: white; width: 150px;"
            }
        )
    )