from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from fitness.celery import app
from fitness.settings import EMAIL_HOST_USER
from subscription.models import SubscriptionFitnessVideo


@app.task
def check_time_subscriptions_finish():
    current_date = datetime.now()
    subscriptions_to_deactivate = SubscriptionFitnessVideo.objects.filter(data_finish__lt=current_date, active=True)
    for subscription in subscriptions_to_deactivate:
        subscription.active = False
        subscription.save()
        print(subscription)


@app.task
def send_welcome_email_task(email, password, sub_type, expire_date_str):
    """
    Таск Celery для отправки письма с данными входа в зависимости от типа подписки.
    """
    subject = "Ваши данные для входа на сайт SIMONA SOLODUHA"

    # Шаблоны ссылок
    if sub_type == 'type_04':
        link_url = "https://simonasoloduha.ru/video/timetable_marathon/"
        link_text = f"Марафон по ссылке: {link_url}"
        link_html = f'Марафон по ссылке: <a href="{link_url}">{link_url}</a>'
    elif sub_type == 'type_05':
        link_url = "https://simonasoloduha.ru/video/timetable/"
        link_text = f"Программа по ссылке и на вкладках: ПРОГРАММЫ и ДЛЯ НАЧИНАЮЩИХ: {link_url}"
        link_html = f'Программа по ссылке и на вкладках: <b>ПРОГРАММЫ</b> и <b>ДЛЯ НАЧИНАЮЩИХ</b>: <a href="{link_url}">{link_url}</a>'
    else:
        link_url = "https://simonasoloduha.ru/video/timetable/"
        link_text = f"Программа по ссылке и на вкладке ПРОГРАММЫ: {link_url}"
        link_html = f'Программа по ссылке и на вкладке <b>ПРОГРАММЫ</b>: <a href="{link_url}">{link_url}</a>'

    # Текстовая версия письма (для почтовых клиентов без HTML)
    text_message = (
        f"Ваши данные для входа на сайт SIMONA SOLODUHA\n\n\n"
        f"почта: {email}\n"
        f"пароль: {password}\n\n\n"
        f"Страница входа: https://simonasoloduha.ru/auth/login_fitness\n\n"
        f"{link_text}\n\n"
        f"Доступ до {expire_date_str}\n\n"
        f"Хороших тренировок и результатов 😘\n\n"
        f"Если будут вопросы — пишите 🌸"
    )

    # Красивая HTML-версия письма для удобного копирования пользователем
    html_message = f"""
    <div style="font-family: Arial, sans-serif; font-size: 15px; color: #222; line-height: 1.6; max-width: 600px;">
        <h2 style="font-size: 18px; font-weight: bold; margin-bottom: 20px;">Ваши данные для входа на сайт SIMONA SOLODUHA</h2>

        <div style="background-color: #f4f4f6; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 20px; user-select: all;">
            <p style="margin: 0 0 8px 0;"><b>Почта:</b> {email}</p>
            <p style="margin: 0;"><b>Пароль:</b> {password}</p>
        </div>

        <p style="margin-bottom: 12px;"><b>Страница входа:</b> <a href="https://simonasoloduha.ru/auth/login_fitness">https://simonasoloduha.ru/auth/login_fitness</a></p>
        <p style="margin-bottom: 12px;">{link_html}</p>
        <p style="margin-bottom: 20px;"><b>Доступ до:</b> {expire_date_str}</p>

        <p style="margin-bottom: 5px;">Хороших тренировок и результатов 😘</p>
        <p style="margin-top: 0; color: #666;">Если будут вопросы — пишите 🌸</p>
    </div>
    """

    mail_sent = send_mail(
        subject=subject,
        message=text_message,
        html_message=html_message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return mail_sent
