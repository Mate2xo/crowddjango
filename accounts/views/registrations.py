from django.shortcuts import redirect, render
from returns.pipeline import is_successful

from accounts.forms import LegalProfileForm, NaturalProfileForm, ProfileForm, SignUpForm
from accounts.services import UserRegistration


def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = __selected_profile_type(request.POST['profile_type'])(request.POST)
        if is_successful(UserRegistration.perform(user_form, profile_form)):
            return redirect('login')
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request,
                  'registration/signup.html',
                  {'user_form': user_form, 'profile_form': profile_form})


def __selected_profile_type(selected_type):
    if selected_type == 'Legal':
        return LegalProfileForm
    elif selected_type == 'Natural':
        return NaturalProfileForm
    else:
        return ProfileForm
