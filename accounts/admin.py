from django.contrib import admin
from .models import LegalProfile, NaturalProfile

admin.site.register([LegalProfile, NaturalProfile])
