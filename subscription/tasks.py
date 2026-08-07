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

@app.task(name='send_welcome_email_task')
def send_welcome_email_task(email, password=None, sub_type=None, expire_date_str=None, is_registered=False):
    """
    Таск Celery для отправки письма о подписке.
    Если is_registered=True (или password пустой), отправляет письмо БЕЗ пароля и ссылки на логин.
    """
    try:
        email = str(email) if email else ""
        password = str(password) if password else ""
        sub_type = str(sub_type) if sub_type else ""
        expire_date_str = str(expire_date_str) if expire_date_str else ""

        # Формируем ссылки в зависимости от типа подписки
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

        # Логика разделения: Новичок VS Зарегистрированный пользователь
        if is_registered or not password:
            # Вариант для зарегистрированного пользователя
            subject = "Ваша подписка на сайте SIMONA SOLODUHA активирована"

            text_message = (
                f"Ваша подписка на сайте SIMONA SOLODUHA успешно оформлена!\n\n\n"
                f"{link_text}\n\n"
                f"Доступ до {expire_date_str}\n\n"
                f"Хороших тренировок и результатов 😘\n\n"
                f"Если будут вопросы — пишите 🌸"
            )

            html_message = f"""
            <div style="font-family: Arial, sans-serif; font-size: 15px; color: #222; line-height: 1.6; max-width: 600px;">
                <h2 style="font-size: 18px; font-weight: bold; margin-bottom: 20px;">Ваша подписка активирована</h2>
                <p style="margin-bottom: 15px;">{link_html}</p>
                <p style="margin-bottom: 20px;"><b>Доступ до:</b> {expire_date_str}</p>
                <p style="margin-bottom: 5px;">Хороших тренировок и результатов 😘</p>
                <p style="margin-top: 0; color: #666;">Если будут вопросы — пишите 🌸</p>
            </div>
            """
        else:
            # Вариант для нового пользователя (с паролем и ссылкой на вход)
            subject = "Ваши данные для входа на сайт SIMONA SOLODUHA"

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

            html_message = f"""
            <div style="font-family: Arial, sans-serif; font-size: 15px; color: #222; line-height: 1.6; max-width: 600px;">
                <h2 style="font-size: 18px; font-weight: bold; margin-bottom: 20px;">Ваши данные для входа на сайт SIMONA SOLODUHA</h2>
                <div style="background-color: #f4f4f6; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 20px;">
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

        return send_mail(
            subject=subject,
            message=text_message,
            html_message=html_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке письма подписки: {e}", exc_info=True)
        raise e
