import os
import logging
from datetime import datetime
from django.core.mail import send_mail
from fitness.celery import app
from fitness.settings import EMAIL_HOST_USER
from subscription.models import SubscriptionFitnessVideo

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage

logger = logging.getLogger(__name__)


@app.task
def check_time_subscriptions_finish():
    current_date = datetime.now()
    subscriptions_to_deactivate = SubscriptionFitnessVideo.objects.filter(data_finish__lt=current_date, active=True)
    for subscription in subscriptions_to_deactivate:
        subscription.active = False
        subscription.save()
        print(subscription)


def get_welcome_email_content(email, password=None, sub_type=None, expire_date_str=""):
    """Вспомогательная функция сборки текста и HTML письма"""
    if sub_type == 'type_04':
        link_url = "https://simonasoloduha.ru/video/timetable_marathon/"
        link_text = f"Марафон по ссылке: {link_url}"
    elif sub_type == 'type_05':
        link_url = "https://simonasoloduha.ru/video/timetable/"
        link_text = f"Программа по ссылке и на вкладках: ПРОГРАММЫ и ДЛЯ НАЧИНАЮЩИХ: {link_url}"
    else:
        link_url = "https://simonasoloduha.ru/video/timetable/"
        link_text = f"Программа по ссылке и на вкладке ПРОГРАММЫ: {link_url}"

    if password:
        subject = "Ваши данные для входа на сайт SIMONA SOLODUHA"
        message_text = (
            f"Ваши данные для входа на сайт SIMONA SOLODUHA\n\n\n"
            f"почта: {email}\n"
            f"пароль: {password}\n\n\n"
            f"Страница входа: https://simonasoloduha.ru/auth/login_fitness\n\n"
            f"{link_text}\n\n"
            f"Доступ до {expire_date_str}\n\n"
            f"Хороших тренировок и результатов 😘\n\n"
            f"Если будут вопросы — пишите, Слоник на все ответит\n\n\n"
            f"С уважением, Симона Солодуха и Слон."
        )
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                <h2>Ваши данные для входа на сайт SIMONA SOLODUHA</h2>
                <p><b>Почта:</b> {email}<br>
                <b>Пароль:</b> {password}</p>
                <p><b>Страница входа:</b> <a href="https://simonasoloduha.ru/auth/login_fitness">https://simonasoloduha.ru/auth/login_fitness</a></p>
                <p><a href="{link_url}">{link_text}</a></p>
                <p><b>Доступ до:</b> {expire_date_str}</p>
                <p>Хороших тренировок и результатов 😘</p>
                <p>Если будут вопросы — пишите, Слоник на все ответит 🐘</p>
                <br>
                <p><img src="cid:slon_image" alt="Слоник" style="max-width: 250px; height: auto; border-radius: 8px;"></p>
                <br>
                <p>С уважением,<br><b>Симона Солодуха и Слон.</b></p>
            </body>
        </html>
        """
    else:
        subject = "Ваша подписка на сайте SIMONA SOLODUHA активирована"
        message_text = (
            f"Ваша подписка на сайте SIMONA SOLODUHA успешно оформлена!\n\n\n"
            f"{link_text}\n\n"
            f"Доступ до {expire_date_str}\n\n"
            f"Хороших тренировок и результатов 😘\n\n"
            f"Если будут вопросы — пишите, Слоник на все ответит\n\n\n"
            f"С уважением, Симона Солодуха и Слон."
        )
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                <h2>Ваша подписка на сайте SIMONA SOLODUHA успешно оформлена!</h2>
                <p><a href="{link_url}">{link_text}</a></p>
                <p><b>Доступ до:</b> {expire_date_str}</p>
                <p>Хороших тренировок и результатов 😘</p>
                <p>Если будут вопросы — пишите, Слоник на все ответит 🐘</p>
                <br>
                <p><img src="cid:slon_image" alt="Слоник" style="max-width: 250px; height: auto; border-radius: 8px;"></p>
                <br>
                <p>С уважением,<br><b>Симона Солодуха и Слон.</b></p>
            </body>
        </html>
        """

    return subject, message_text, html_content


@app.task(time_limit=30, soft_time_limit=20)
def send_welcome_email_task(email, password=None, sub_type=None, expire_date_str=""):
    """Таск Celery отправки письма о подписке с фото слоника"""

    subject, message_text, html_content = get_welcome_email_content(email, password, sub_type, expire_date_str)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=message_text,
        from_email=EMAIL_HOST_USER,
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")

    # Путь к файлу картинки в static
    image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'SLON.png')

    if os.path.exists(image_path):
        with open(image_path, 'rb') as img:
            mime_image = MIMEImage(img.read())
            # Указываем Content-ID, чтобы связать с <img src="cid:slon_image">
            mime_image.add_header('Content-ID', '<slon_image>')
            mime_image.add_header('Content-Disposition', 'inline', filename='SLON.png')
            msg.attach(mime_image)

    return msg.send()

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
#             f"Если будут вопросы — пишите, Слоник на все ответит\n\n\n"
#             f"C уважением, Симона Солодуха и Слон."
#         )
#     else:
#         subject = "Ваша подписка на сайте SIMONA SOLODUHA активирована"
#         message = (
#             f"Ваша подписка на сайте SIMONA SOLODUHA успешно оформлена!\n\n\n"
#             f"{link_text}\n\n"
#             f"Доступ до {expire_date_str}\n\n"
#             f"Хороших тренировок и результатов 😘\n\n"
#             f"Если будут вопросы — пишите 🌸"
#             f"Если будут вопросы — пишите, Слоник на все ответит\n\n\n"
#             f"C уважением, Симона Солодуха и Слон."
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
