from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class CustomEmailBackend(ModelBackend):

    """
    Авторизация через email
    """

    def authenticate(self, request, **kwargs):
        email_or_username = kwargs['username']
        password = kwargs['password']

        try:
            if '@' in email_or_username:
                user = User.objects.get(email=email_or_username)
            else:
                user = User.objects.get(username=email_or_username)
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            return None
