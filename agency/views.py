from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import (
    RedactorCreationForm,
    RedactorExperienceUpdateForm,
    NewspaperCustomForm,
    TopicCustomForm, TopicSearchForm, RedactorSearchForm, NewspaperSearchForm
)
from agency.models import Redactor, Newspaper, Topic


@login_required
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


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 5

    def get_queryset(self):
        queryset = Topic.objects.all()
        form = TopicSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = TopicSearchForm(
            initial={"name": name}
        )
        return context


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = TopicCustomForm
    model = Topic
    success_url = reverse_lazy("agency:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    fields = "__all__"
    model = Topic
    success_url = reverse_lazy("agency:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("agency:topic-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_by = form.cleaned_data["search_by"]

            if query:
                if search_by == "username":
                    queryset = queryset.filter(username__icontains=query)
                elif search_by == "first_name":
                    queryset = queryset.filter(first_name__icontains=query)
                elif search_by == "last_name":
                    queryset = queryset.filter(last_name__icontains=query)
                elif search_by == "years_of_experience":
                    queryset = queryset.filter(years_of_experience__icontains=query)
                elif search_by == "all":
                    queryset = queryset.filter(
                        Q(username__icontains=query) |
                        Q(first_name__icontains=query) |
                        Q(last_name__icontains=query) |
                        Q(years_of_experience__icontains=query)
                    )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RedactorSearchForm(self.request.GET)
        context["search_form"] = form
        return context


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("agency:redactor-list")


class RedactorExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorExperienceUpdateForm
    success_url = reverse_lazy("agency:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("agency:redactor-list")


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.prefetch_related("topic", "publishers")
    paginate_by = 5

    def get_queryset(self):
        queryset = Newspaper.objects.all()
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_by = form.cleaned_data["search_by"]

            if query:
                if search_by == "title":
                    queryset = queryset.filter(title__icontains=query)
                elif search_by == "content":
                    queryset = queryset.filter(content__icontains=query)
                elif search_by == "published_date":
                    queryset = queryset.filter(published_date__icontains=query)
                elif search_by == "topic":
                    queryset = queryset.filter(topic__name__icontains=query)
                elif search_by == "publisher_username":
                    queryset = queryset.filter(publishers__username__icontains=query)
                elif search_by == "publisher_first_name":
                    queryset = queryset.filter(publishers__first_name__icontains=query)
                elif search_by == "publisher_last_name":
                    queryset = queryset.filter(publishers__last_name__icontains=query)
                elif search_by == "all":
                    queryset = queryset.filter(
                        Q(title__icontains=query) |
                        Q(content__icontains=query) |
                        Q(published_date__icontains=query) |
                        Q(topic__name__icontains=query) |
                        Q(publishers__username__icontains=query) |
                        Q(publishers__first_name__icontains=query) |
                        Q(publishers__last_name__icontains=query) |
                        Q(all__icontains=query)
                    )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = NewspaperSearchForm(self.request.GET)
        context["search_form"] = form
        return context


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperCustomForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperCustomForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
