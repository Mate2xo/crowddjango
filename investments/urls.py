from django.urls import path
from investments.views import funds, subscriptions

app_name = 'investments'
urlpatterns = [
    path('funds/', funds.List.as_view(), name='funds_list'),
    path('funds/<int:pk>', funds.Detail.as_view(), name='fund_detail'),
    path('dashboard/', subscriptions.List.as_view(), name='dashboard'),
    path('subscriptions/<int:pk>', subscriptions.Detail.as_view(), name='subscription_detail')
]
