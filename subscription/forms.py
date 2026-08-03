import string
import secrets
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from subscription.models import Subscription, SubscriptionFitnessVideo, TYPE_CHOICES

# from .models import TYPE_CHOICES  # Укажите точный импорт choices вашей подписки

User = get_user_model()


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


class AdminRegisterWithSubscriptionForm(forms.Form):
    email = forms.EmailField(
        label=_('Email пользователя'),
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}
        ),
    )
    sub_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        label=_('Тип / Номер подписки'),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('Пользователь с таким e-mail уже зарегистрирован.')
            )
        return email

    def generate_random_password(self, length=12):
        """Генерация надежного случайного пароля"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))