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
    # mail_sent = send_mail(
    #     _('Вперед к тренировкам! Твоя подписка оформленна'),
    #     _(f'Это куда идет?'),
    #     EMAIL_HOST_USER,
    #     [email_user],
    #     fail_silently=False,
    #     html_message=loader.render_to_string('email_lists/subscriptions_start/subscriptions_start.html')
    # )

    body_html = loader.render_to_string('email_lists/subscriptions_start/subscriptions_start.html')

    msg = EmailMultiAlternatives(
        _('Вперед к тренировкам! Твоя подписка оформленна'),
        body_html,
        from_email=EMAIL_HOST_USER,
        to=['ls460simona@gmail.com']
    )

    msg.mixed_subtype = 'related'
    msg.attach_alternative(body_html, "text/html")
    img_dir = 'templates/email_lists/subscriptions_start/images'
    image = 'youtube2x.png'
    file_path = os.path.join(img_dir, image)
    with open(file_path, 'rb') as f:
        print('file_path', file_path)
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)
    msg.attach(img)
    msg.send()
    # return msg
