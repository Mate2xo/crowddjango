from django.contrib import admin
from .models import Fund, Subscription

admin.site.register([Fund, Subscription])
