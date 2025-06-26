from datetime import datetime

from fitness.celery import app
from fitness.settings import EMAIL_HOST_USER
from django.utils.translation import gettext_lazy as _
from django.template import loader

from django.core.mail import EmailMultiAlternatives

from subscription.models import SubscriptionFitnessVideo

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
        to=[email_user, 'ls460simona@gmail.com']
    )
    msg.attach_alternative(body_html, "text/html")
    mail_sent = msg.send()
    return mail_sent


@app.task
def check_time_subscriptions_finish():
    current_date = datetime.now()
    subscriptions_to_deactivate = SubscriptionFitnessVideo.objects.filter(data_finish__lt=current_date, active=True)
    for subscription in subscriptions_to_deactivate:
        subscription.active = False
        subscription.save()
        print(subscription)
