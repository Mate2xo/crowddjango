from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

class Profile(PolymorphicModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

class Legal(Profile):
    name = models.CharField(max_length=200)
    legal_representative_first_name = models.CharField(max_length=200)
    legal_representative_last_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name or f'{self.user.first_name} {self.user.last_name}'.strip()

    class Meta:
        verbose_name = _('legal entity')
        verbose_name_plural = _('legal entities')

class Natural(Profile):
    place_of_birth = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'.strip()

    class Meta:
        verbose_name = _('natural person')
        verbose_name_plural = _('natural persons')
