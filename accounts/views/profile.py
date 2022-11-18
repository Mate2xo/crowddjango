from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from accounts.models import Legal, Natural


class ProfileDetail(LoginRequiredMixin, DetailView):
    def setup(self, request, *args, **kwargs):
        if not self.model:
            self.model = request.user.profile.__class__
        return super().setup(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.profile


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    def setup(self, request, *args, **kwargs):
        self.model = request.user.profile.__class__
        self.fields = EDITABLE_FIELDS[self.model]
        return super().setup(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.profile


EDITABLE_FIELDS = {
    Legal: [
        'email',
        'phone_number',
        'name',
        'legal_representative_first_name',
        'legal_representative_last_name'
    ],
    Natural: [
        'email',
        'phone_number',
        'place_of_birth'
    ]
}
