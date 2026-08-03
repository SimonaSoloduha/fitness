from datetime import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

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


@shared_task
def send_welcome_email_task(email, password, sub_type, expire_date_str):
    """
    Таск Celery для отправки письма с данными входа в зависимости от типа подписки.
    """
    subject = "Ваши данные для входа на сайт SIMONA SOLODUHA"

    # Шаблон 1: для type_04 (Марафон)
    if sub_type == 'type_04':
        link_text = f"Марафон по ссылке: https://simonasoloduha.ru/video/timetable_marathon/"
    # Шаблон 2: для type_05 (Программы и Для начинающих)
    elif sub_type == 'type_05':
        link_text = f"Программа по ссылке и на вкладках: ПРОГРАММЫ и ДЛЯ НАЧИНАЮЩИХ: https://simonasoloduha.ru/video/timetable/"
    # Шаблон 3: для всех остальных (type_00, type_01, type_02, type_03, type_06 и т.д.)
    else:
        link_text = f"Программа по ссылке и на вкладке ПРОГРАММЫ: https://simonasoloduha.ru/video/timetable/"

    # Собираем полное тело письма
    message = (
        f"Ваши данные для входа на сайт SIMONA SOLODUHA\n\n\n"
        f"почта: {email}\n"
        f"пароль: {password}\n\n\n"
        f"Страница входа: https://simonasoloduha.ru/auth/login_fitness\n\n"
        f"{link_text}\n\n"
        f"Доступ до {expire_date_str}\n\n"
        f"Хороших тренировок и результатов 😘\n\n"
        f"Если будут вопросы — пишите 🌸"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Убедитесь, что заполнено в settings.py
        recipient_list=[email],
        fail_silently=False,
    )