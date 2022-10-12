from django.db import models
from django.contrib.auth.models import User

class Legal(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    legal_representative_first_name = models.CharField(max_length=200)
    legal_representative_last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Natural(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    place_of_birth = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
