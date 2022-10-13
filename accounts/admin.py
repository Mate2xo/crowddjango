from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import LegalProfile, NaturalProfile

admin.site.register([LegalProfile, NaturalProfile])

class LegalProfileInline(admin.StackedInline):
    model = LegalProfile
    can_delete = False
    verbose_name_plural = 'legal profiles'

class NaturalProfileInline(admin.StackedInline):
    model = NaturalProfile
    can_delete = False
    verbose_name_plural = 'natural profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (LegalProfileInline, NaturalProfileInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
