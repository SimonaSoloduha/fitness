import os

from django.core.mail import send_mail

from fitness.celery import app
from fitness.settings import EMAIL_HOST_USER
from django.utils.translation import gettext_lazy as _
from django.template import loader

from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives


@app.task
def send_hello_to_email(email_user):
    """
    Отправка письма с подтверждением подписки
    """

    body_html = loader.render_to_string('email_lists/subscriptions_start/subscription.html')

    msg = EmailMultiAlternatives(
        _('Добро пожаловать в СПОРТ 🌸'),
        body_html,
        from_email=EMAIL_HOST_USER,
        to=[email_user]
    )
    msg.attach_alternative(body_html, "text/html")
    mail_sent = msg.send()
    return mail_sent
