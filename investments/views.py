from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Subscription

class SubscriptionsList(LoginRequiredMixin, generic.ListView):
    model = Subscription

    def get_queryset(self):
        return self.request.user.profile.subscription_set.all()

class SubscriptionDetail(LoginRequiredMixin, generic.DetailView):
    model = Subscription
