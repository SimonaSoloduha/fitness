from django import forms

from subscription.models import Subscription, SubscriptionFitnessVideo


class SubscriptionForm(forms.ModelForm):
    """ Форма подписки """

    class Meta:
        model = Subscription
        fields = ['email', ]


class SubscriptionFitnessVideoForm(forms.ModelForm):
    """ Форма платной подписки"""

    class Meta:
        model = SubscriptionFitnessVideo
        fields = ['promo_code', ]
