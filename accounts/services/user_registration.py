from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from returns import result, pointfree, pipeline

from accounts.models import Legal, Natural


class UserRegistration():
    @classmethod
    def perform(cls, form: UserCreationForm) -> result.Success | result.Failure:
        with transaction.atomic():
            return pipeline.flow(
                form,
                cls.validate_form,
                pointfree.bind(cls.create_user),
                pointfree.bind(cls.create_user_profile)
            )

    @classmethod
    def validate_form(cls, form: UserCreationForm) -> result.Result[UserCreationForm, UserCreationForm]:
        if form.is_valid():
            return result.Success(form)
        else:
            return result.Failure(form)

    @classmethod
    def create_user(cls, form: UserCreationForm):
        user = form.save()
        return result.Success({'user': user, 'form': form})

    @classmethod
    def create_user_profile(cls, input) -> result.Result[UserCreationForm, UserCreationForm]:
        profile_type = input['form'].cleaned_data['profile_type']
        if profile_type == 'Legal':
            Legal(user=input['user']).save()
            return result.Success(input['user'])
        elif profile_type == 'Natural':
            Natural(user=input['user']).save()
            return result.Failure(input['user'])
