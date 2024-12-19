from django.urls import path

from subscription.views import subscription, subscription_fit_vid_promocode

urlpatterns = [
    path('subscription/', subscription, name='subscription'),
    path('subscription/subscription_fit_vid_promocode', subscription_fit_vid_promocode, name='subscription_fit_vid_promocode')

]
