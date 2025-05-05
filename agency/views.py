from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

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