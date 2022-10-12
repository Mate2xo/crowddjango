from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .models import LegalProfile, NaturalProfile
from .forms import SignUpForm

@login_required()
def profile(request):
    return HttpResponse("Profile page")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            associate_user_and_profile(user, form)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', { 'form': form })

def associate_user_and_profile(user, form):
    profile_type = form.cleaned_data['profile_type']
    if profile_type == 'Legal':
        LegalProfile(user=user).save()
    elif profile_type == 'Natural':
        NaturalProfile(user=user).save()
