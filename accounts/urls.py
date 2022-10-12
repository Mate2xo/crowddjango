from django.urls import include, path

from .views import profiles

urlpatterns = [
    path('profile/', profiles.show, name='profile_show')
]
