from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .services import UserRegistration

@login_required()
def profile(request):
    return HttpResponse("Profile page")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if UserRegistration.perform(form):
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', { 'form': form })
