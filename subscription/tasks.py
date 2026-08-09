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


def get_welcome_email_content(email, password=None, sub_type=None, expire_date_str=""):
    """Вспомогательная функция сборки текста письма и блока копирования"""
    if sub_type == 'type_04':
        link_text = "Марафон по ссылке: https://simonasoloduha.ru/video/timetable_marathon/"
    elif sub_type == 'type_05':
        link_text = "Программа по ссылке и на вкладках: ПРОГРАММЫ и ДЛЯ НАЧИНАЮЩИХ: https://simonasoloduha.ru/video/timetable/"
    else:
        link_text = "Программа по ссылке и на вкладке ПРОГРАММЫ: https://simonasoloduha.ru/video/timetable/"

    if password:
        subject = "Ваши данные для входа на сайт SIMONA SOLODUHA"
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
    else:
        subject = "Ваша подписка на сайте SIMONA SOLODUHA активирована"
        message = (
            f"Ваша подписка на сайте SIMONA SOLODUHA успешно оформлена!\n\n\n"
            f"{link_text}\n\n"
            f"Доступ до {expire_date_str}\n\n"
            f"Хороших тренировок и результатов 😘\n\n"
            f"Если будут вопросы — пишите 🌸"
        )

    return subject, message


@app.task(time_limit=30, soft_time_limit=20)
def send_welcome_email_task(email, password=None, sub_type=None, expire_date_str=""):
    """Таск Celery отправки письма о подписке"""
    try:
        subject, message = get_welcome_email_content(email, password, sub_type, expire_date_str)

        return send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке письма подписки: {e}", exc_info=True)
        raise e
