from django.core.mail import settings
from django.db import transaction
from returns import result, pointfree, pipeline
from templated_email import send_templated_mail

from accounts.forms import LegalProfileForm, NaturalProfileForm, SignUpForm
from accounts.tasks import send_welcome_email_task


class UserRegistration():
    @classmethod
    def perform(cls,
                user_form: SignUpForm,
                profile_form: LegalProfileForm | NaturalProfileForm
                ) -> result.Success | result.Failure:
        with transaction.atomic():
            return pipeline.flow(
                {'user_form': user_form, 'profile_form': profile_form},
                cls.validate_form,
                pointfree.bind(cls.create_user),
                pointfree.bind(cls.create_user_profile),
                pointfree.map_(cls.send_welcome_email)
            )

    @classmethod
    def validate_form(cls, input: dict) -> result.Result:
        user, profile = input['user_form'], input['profile_form']
        if user.is_valid() and profile.is_valid():
            return result.Success(input)
        else:
            return result.Failure({'errors': {**user.errors, **profile.errors}})

    @classmethod
    def create_user(cls, input: dict) -> result.Success:
        input['user'] = input['user_form'].save()
        return result.Success(input)

    @classmethod
    def create_user_profile(cls, input: dict) -> result.Success:
        profile_form = input['profile_form']
        profile_form.instance.user = input['user']
        input['profile'] = profile_form.save()
        return result.Success(input)

    @classmethod
    def send_welcome_email(cls, input: dict) -> None:
        return send_welcome_email_task.delay(to=input['profile'].email)
