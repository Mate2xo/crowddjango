from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import LegalProfile, NaturalProfile

class Fund(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    amount = models.PositiveIntegerField()
    legal_profile = models.ForeignKey(LegalProfile, on_delete=models.PROTECT, null=True, blank=True)
    natural_profile = models.ForeignKey(NaturalProfile, on_delete=models.PROTECT, null=True, blank=True)
    fund = models.ForeignKey(Fund, on_delete=models.PROTECT)

    def clean(self):
        if self.legal_profile is None and self.natural_profile is None:
            raise ValidationError('A legal profile or a natural profile must be selected')
        if self.legal_profile and self.natural_profile:
            raise ValidationError('A legal profile OR a natural profile must be selected')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        profile = self.legal_profile or self.natural_profile
        full_name = f'{profile.user.first_name} {profile.user.last_name}'.strip()

        return full_name or profile.user.username
