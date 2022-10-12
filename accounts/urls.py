from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile_show'),
    path('signup/', views.signup, name='signup')
]
