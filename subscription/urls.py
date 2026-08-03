from django.urls import path

from subscription.views import subscription, subscription_fit_vid_promocode, payment_subscription_fit_vid, \
    PaymentSubscriptionDetailView, register_user_with_subscription

urlpatterns = [
    path('subscription/', subscription, name='subscription'),
    path('subscription/subscription_fit_vid_promocode', subscription_fit_vid_promocode,
         name='subscription_fit_vid_promocode'),
    path('subscription/payment_subscription_fit_vid', payment_subscription_fit_vid,
         name='payment_subscription_fit_vid'),
    path('subscription/payment_subscription_fit_vid/<slug:pk>/', PaymentSubscriptionDetailView.as_view(),
         name='payment_subscription_fit_vid_detail'),
    path(
            'admin-panel/register-user-sub/',
            register_user_with_subscription,
            name='register_with_subscription',
        ),
]
