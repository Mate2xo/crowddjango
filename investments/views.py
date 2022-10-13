from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Subscription

class SubscriptionsList(LoginRequiredMixin, generic.ListView):
    model = Subscription

class SubscriptionDetail(LoginRequiredMixin, generic.DetailView):
    model = Subscription
