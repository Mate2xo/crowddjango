from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicParentModelAdmin,
    PolymorphicInlineSupportMixin,
    StackedPolymorphicInline
)

from .models import Legal, Natural, Profile

@admin.register(Profile)
class ProfileParentAdmin(PolymorphicParentModelAdmin):
    base_model = Profile
    child_models = (Legal, Natural)
    polymorphic_list = True

@admin.register(Natural)
class LegalAdmin(PolymorphicChildModelAdmin):
    base_model = Legal

@admin.register(Legal)
class NaturalAdmin(PolymorphicChildModelAdmin):
    base_model = Natural

class ProfileInline(StackedPolymorphicInline):
    class LegalProfileInline(StackedPolymorphicInline.Child):
        model = Legal

    class NaturalProfileInline(StackedPolymorphicInline.Child):
        model = Natural

    model = Profile
    child_inlines = (LegalProfileInline, NaturalProfileInline)

class UserAdmin(PolymorphicInlineSupportMixin, BaseUserAdmin):
    inlines = (ProfileInline,)

# # Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
