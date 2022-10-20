from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    # Translators: On the sign-up form, the user must choose if their account is made on behalf of a company, or for a real person
    profile_type = forms.ChoiceField(choices = [('Legal', _('legal entity')), ('Natural', _('natural person'))])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
