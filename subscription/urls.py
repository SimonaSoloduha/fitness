from django.urls import path

from subscription.views import subscription

urlpatterns = [
    path('subscription/', subscription, name='subscription')
]
