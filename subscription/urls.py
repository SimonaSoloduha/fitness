from django.urls import path

from subscription.views import subscription

urlpatterns = [
    # path('', SubscriptionView.as_view(), name='subscription')
    path('subscription/', subscription, name='subscription')

]
