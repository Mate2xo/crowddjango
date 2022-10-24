from django.urls import path
from . import views

app_name = 'investments'
urlpatterns = [
    path('dashboard/', views.SubscriptionsList.as_view(), name='dashboard'),
    path('subscriptions/<int:pk>', views.SubscriptionDetail.as_view(), name='subscription_detail')
]
