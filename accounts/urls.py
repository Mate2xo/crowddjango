from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.profile, name='profile_show'),
    path('signup/', views.signup, name='signup')
]
