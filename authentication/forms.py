from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from authentication.models import Code


class RegisterForm(UserCreationForm):
    """
    Форма регистрации
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ResetPassword1(forms.Form):
    """
    Форма восстановления пароля, шаг 1 - введение email
    """

    email = forms.CharField(label=_('email'), help_text=_('Введите email'))


class CodeForm(forms.ModelForm):
    """
    Форма восстановления пароля, шаг 2 - введение кода, отправленного на email
    """
    number = forms.CharField(label=_('Код подтверждения'), help_text=_('Введите код, отправленный на email'))

    class Meta:
        model = Code
        fields = ('number',)


class CustomSetPasswordForm(forms.Form):
    """
    Форма восстановления пароля, шаг 3 - введение нового пароля
    """

    error_messages = {
        "password_mismatch": _("Пароли не совпадают"),
    }
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Повторите пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
