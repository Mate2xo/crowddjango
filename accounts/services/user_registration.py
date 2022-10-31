from django.contrib.auth.forms import UserCreationForm

from accounts.models import Legal, Natural

class UserRegistration():
    @classmethod
    def perform(cls, form: UserCreationForm) -> bool:
        if not form.is_valid():
            return False

        user = form.save()
        cls.__associate_user_and_profile(user, form)

        return True

    @classmethod
    def __associate_user_and_profile(cls, user, form):
        profile_type = form.cleaned_data['profile_type']
        if profile_type == 'Legal':
            Legal(user=user).save()
        elif profile_type == 'Natural':
            Natural(user=user).save()
