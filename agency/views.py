from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import RedactorCreationForm, RedactorExperienceUpdateForm, NewspaperCustomForm
from agency.models import Redactor, Newspaper, Topic


def index(request):
    """View function for the home page of the site."""

    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "agency/index.html", context=context)


class TopicListView(generic.ListView):
    model = Topic


class TopicCreateView(generic.CreateView):
    fields = "__all__"
    model = Topic
    success_url = reverse_lazy("agency:topic-list")


class TopicUpdateView(generic.UpdateView):
    fields = "__all__"
    model = Topic
    success_url = reverse_lazy("agency:topic-list")


class TopicDeleteView(generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("agency:topic-list")


class RedactorListView(generic.ListView):
    model = Redactor


class RedactorCreateView(generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("agency:redactor-list")


class RedactorExperienceUpdateView(generic.UpdateView):
    model = Redactor
    form_class = RedactorExperienceUpdateForm
    success_url = reverse_lazy("agency:redactor-list")


class RedactorDeleteView(generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("agency:redactor-list")


class RedactorDetailView(generic.DetailView):
    model = Redactor


class NewspaperListView(generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.prefetch_related("topic", "publishers")


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    form_class = NewspaperCustomForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    form_class = NewspaperCustomForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDeleteView(generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
