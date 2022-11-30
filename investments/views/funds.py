from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from investments.models import Fund


class List(LoginRequiredMixin, generic.ListView):
    model = Fund


class Detail(LoginRequiredMixin, generic.DetailView):
    model = Fund
