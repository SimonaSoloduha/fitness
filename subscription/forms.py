from django import forms

from subscription.models import Subscription


class SubscriptionForm(forms.ModelForm):
    """ Форма подписки """

    class Meta:
        model = Subscription
        fields = ['email', ]
