from django.urls import path

from .views import profile, registrations

app_name = 'accounts'
urlpatterns = [
    path('profile/', profile.ProfileDetail.as_view(), name='profile_show'),
    path('profile/edit', profile.ProfileUpdate.as_view(), name='profile_edit'),
    path('signup/', registrations.signup, name='signup')
]
