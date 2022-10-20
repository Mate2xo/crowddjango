from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile

class Fund(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('fund')
        verbose_name_plural = _('funds')

class Subscription(models.Model):
    amount = models.PositiveIntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    fund = models.ForeignKey(Fund, on_delete=models.PROTECT)

    def __str__(self):
        full_name = f'{self.profile.user.first_name} {self.profile.user.last_name}'.strip()

        return full_name or self.profile.user.username

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
