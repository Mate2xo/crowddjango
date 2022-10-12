from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    profile_type = forms.ChoiceField(choices = [('Legal', 'Personne morale'), ('Natural', 'Personne physique')])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
