from django.db import models
from django.contrib.auth.models import User

class LegalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    legal_representative_first_name = models.CharField(max_length=200)
    legal_representative_last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name or f'{self.user.first_name} {self.user.last_name}'

class NaturalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=20)
    place_of_birth = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
