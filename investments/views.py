from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Subscription
from accounts.models import Profile

class SubscriptionsList(LoginRequiredMixin, generic.ListView):
    model = Subscription

    def get_queryset(self):
        return self.request.user.profile.subscription_set.all()

class SubscriptionDetail(LoginRequiredMixin, generic.DetailView):
    model = Subscription

    def get_object(self):
        try:
            scoped_manager = self.request.user.profile.subscription_set
        except Profile.DoesNotExist:
            raise Http404()
        return get_object_or_404(scoped_manager)
