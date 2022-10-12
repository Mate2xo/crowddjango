from django.urls import include, path

from .views import profiles

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', profiles.show, name='show')
]
