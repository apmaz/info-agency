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
        'placeholder': "Enter title here..."
            }
        ),

        label=mark_safe("<strong>Title</strong>"),
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
            "rows": 5,
            "cols": 25,
            "placeholder": "Enter content here..."
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





























