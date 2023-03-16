from django.core.mail import send_mail

from fitness.celery import app
from fitness.settings import EMAIL_HOST_USER
from django.utils.translation import gettext_lazy as _


@app.task
def send_code_to_email(code_user, email_user):
    """
    Отправка письма с кодом подтверждения
    """
    mail_sent = send_mail(
        _('Код подтверждения'),
        _(f'Ваш код для входа: {code_user}'),
        EMAIL_HOST_USER,
        [email_user],
        fail_silently=False,
    )
    return mail_sent
