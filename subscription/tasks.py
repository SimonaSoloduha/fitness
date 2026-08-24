import logging
from datetime import datetime
from django.core.mail import send_mail
from fitness.celery import app
from fitness.settings import EMAIL_HOST_USER
from subscription.models import SubscriptionFitnessVideo

logger = logging.getLogger(__name__)


@app.task
def check_time_subscriptions_finish():
    current_date = datetime.now()
    subscriptions_to_deactivate = SubscriptionFitnessVideo.objects.filter(data_finish__lt=current_date, active=True)
    for subscription in subscriptions_to_deactivate:
        subscription.active = False
        subscription.save()
        print(subscription)

#
# def get_welcome_email_content(email, password=None, sub_type=None, expire_date_str=""):
#     """Вспомогательная функция сборки текста письма и блока копирования"""
#     if sub_type == 'type_04':
#         link_text = "Марафон по ссылке: https://simonasoloduha.ru/video/timetable_marathon/"
#     elif sub_type == 'type_05':
#         link_text = "Программа по ссылке и на вкладках: ПРОГРАММЫ и ДЛЯ НАЧИНАЮЩИХ: https://simonasoloduha.ru/video/timetable/"
#     else:
#         link_text = "Программа по ссылке и на вкладке ПРОГРАММЫ: https://simonasoloduha.ru/video/timetable/"
#
#     if password:
#         subject = "Ваши данные для входа на сайт SIMONA SOLODUHA"
#         message = (
#             f"Ваши данные для входа на сайт SIMONA SOLODUHA\n\n\n"
#             f"почта: {email}\n"
#             f"пароль: {password}\n\n\n"
#             f"Страница входа: https://simonasoloduha.ru/auth/login_fitness\n\n"
#             f"{link_text}\n\n"
#             f"Доступ до {expire_date_str}\n\n"
#             f"Хороших тренировок и результатов 😘\n\n"
#             f"Если будут вопросы — пишите, Слоник на все ответит 🐘\n"
#             f"С уважением, Симона Солодуха и Слон."
#         )
#     else:
#         subject = "Ваша подписка на сайте SIMONA SOLODUHA активирована"
#         message = (
#             f"Ваша подписка на сайте SIMONA SOLODUHA успешно оформлена!\n\n\n"
#             f"{link_text}\n\n"
#             f"Доступ до {expire_date_str}\n\n"
#             f"Хороших тренировок и результатов 😘\n\n"
#             f"Если будут вопросы — пишите, Слоник на все ответит 🐘\n"
#             f"С уважением, Симона Солодуха и Слон."
#         )
#
#     return subject, message
#
#
# @app.task(time_limit=30, soft_time_limit=20)
# def send_welcome_email_task(email, password=None, sub_type=None, expire_date_str=""):
#     """Таск Celery отправки письма о подписке"""
#
#     subject, message = get_welcome_email_content(email, password, sub_type, expire_date_str)
#
#     mail_sent = send_mail(
#         subject=subject,
#         message=message,
#         from_email=EMAIL_HOST_USER,
#         recipient_list=[email],
#         fail_silently=False,
#     )
#
#     return mail_sent
def get_welcome_email_content(email, password=None, sub_type=None, expire_date_str=""):
    """Вспомогательная функция сборки текста письма и HTML с фото слоника"""
    if sub_type == 'type_04':
        link_url = "https://simonasoloduha.ru/video/timetable_marathon/"
        link_text = f"Марафон по ссылке: {link_url}"
    elif sub_type == 'type_05':
        link_url = "https://simonasoloduha.ru/video/timetable/"
        link_text = f"Программа по ссылке и на вкладках: ПРОГРАММЫ и ДЛЯ НАЧИНАЮЩИХ: {link_url}"
    else:
        link_url = "https://simonasoloduha.ru/video/timetable/"
        link_text = f"Программа по ссылке и на вкладке ПРОГРАММЫ: {link_url}"

    # Прямая ссылка на слоника на вашем сервере
    slon_img_url = "https://simonasoloduha.ru/static/images/SLON.png"

    if password:
        subject = "Ваши данные для входа на сайт SIMONA SOLODUHA"

        # Текстовая версия
        message = (
            f"Ваши данные для входа на сайт SIMONA SOLODUHA\n\n\n"
            f"почта: {email}\n"
            f"пароль: {password}\n\n\n"
            f"Страница входа: https://simonasoloduha.ru/auth/login_fitness\n\n"
            f"{link_text}\n\n"
            f"Доступ до {expire_date_str}\n\n"
            f"Хороших тренировок и результатов 😘\n\n"
            f"Если будут вопросы — пишите, Слоник на все ответит\n\n\n"
            f"C уважением, Симона Солодуха и Слон."
        )

        # HTML-версия с картинкой
        html_message = f"""
        <div style="font-family: Arial, sans-serif; color: #222; line-height: 1.6;">
            <h2>Ваши данные для входа на сайт SIMONA SOLODUHA</h2>
            <p><b>почта:</b> {email}<br>
            <b>пароль:</b> {password}</p>
            <p><b>Страница входа:</b> <a href="https://simonasoloduha.ru/auth/login_fitness">https://simonasoloduha.ru/auth/login_fitness</a></p>
            <p><a href="{link_url}">{link_text}</a></p>
            <p><b>Доступ до:</b> {expire_date_str}</p>
            <p>Хороших тренировок и результатов 😘</p>
            <p>Если будут вопросы — пишите, Слоник на все ответит 🌸</p>
            <div style="margin: 20px 0;">
                <img src="{slon_img_url}" alt="Слоник" style="max-width: 280px; height: auto; border-radius: 12px;">
            </div>
            <p>C уважением, <b>Симона Солодуха и Слон.</b></p>
        </div>
        """
    else:
        subject = "Ваша подписка на сайте SIMONA SOLODUHA активирована"

        # Текстовая версия
        message = (
            f"Ваша подписка на сайте SIMONA SOLODUHA успешно оформлена!\n\n\n"
            f"{link_text}\n\n"
            f"Доступ до {expire_date_str}\n\n"
            f"Хороших тренировок и результатов 😘\n\n"
            f"Если будут вопросы — пишите, Слоник на все ответит\n\n\n"
            f"C уважением, Симона Солодуха и Слон."
        )

        # HTML-версия с картинкой
        html_message = f"""
        <div style="font-family: Arial, sans-serif; color: #222; line-height: 1.6;">
            <h2>Ваша подписка на сайте SIMONA SOLODUHA успешно оформлена!</h2>
            <p><a href="{link_url}">{link_text}</a></p>
            <p><b>Доступ до:</b> {expire_date_str}</p>
            <p>Хороших тренировок и результатов 😘</p>
            <p>Если будут вопросы — пишите, Слоник на все ответит 🌸</p>
            <div style="margin: 20px 0;">
                <img src="{slon_img_url}" alt="Слоник" style="max-width: 280px; height: auto; border-radius: 12px;">
            </div>
            <p>C уважением, <b>Симона Солодуха и Слон.</b></p>
        </div>
        """

    return subject, message, html_message


@app.task(time_limit=30, soft_time_limit=20)
def send_welcome_email_task(email, password=None, sub_type=None, expire_date_str=""):
    """Таск Celery отправки письма о подписке"""

    subject, message, html_message = get_welcome_email_content(email, password, sub_type, expire_date_str)

    mail_sent = send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
        html_message=html_message  # Передаем собранную HTML-структуру с фото
    )

    return mail_sent
