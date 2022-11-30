from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Profile
from investments.models import Fund

class Subscription(models.Model):
    amount = models.PositiveIntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    fund = models.ForeignKey(Fund, on_delete=models.PROTECT)

    def __str__(self):
        return self.profile.get_real_instance().__str__()

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
