from django.contrib import admin
from .models import Legal, Natural

admin.site.register([Legal, Natural])
