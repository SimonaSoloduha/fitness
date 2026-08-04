from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login

from authentication.forms import RegisterForm
from subscription.forms import SubscriptionFitnessVideoForm, AdminRegisterWithSubscriptionForm
from subscription.models import Subscription, SubscriptionFitnessVideo, PromoCodeFitnessVideo, PaymentSubscription
from subscription.tasks import send_hello_to_email, send_welcome_email_task

User = get_user_model()


def subscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            subscription = Subscription.objects.get(email=email)
            if subscription.active:
                message = _('Вы уже подписаны на рассылку')
            else:
                subscription.active = True
                subscription.save()
                send_hello_to_email(email)
                message = _('Ваша подписка оформлена')
        except Subscription.DoesNotExist:
            new = Subscription(email=email)
            new.save()
            send_hello_to_email(email)
            message = _('Ваша подписка оформлена')
        return JsonResponse({'message': message})
    return JsonResponse({'message': 'Invalid request method'}, status=400)


def subscription_fit_vid_promocode(request):
    """
    Представление ввода промокода
    """

    context = {
        'form': SubscriptionFitnessVideoForm(),
    }
    if request.method == "POST":
        promo_code = request.POST.get('promo_code')
        user = request.user
        try:
            promo_code_fit_vid = PromoCodeFitnessVideo.objects.get(code=promo_code)
            user_subscription_fit_vid = (SubscriptionFitnessVideo.objects.
                                         filter(user=user, sub_type__contains=promo_code_fit_vid.sub_type, active=True).
                                         first())

            if user_subscription_fit_vid:
                attention = f'У вас активна такая подписка до {user_subscription_fit_vid.data_finish.strftime("%Y-%m-%d %H:%M:%S")}'
            else:
                user_subscription_fit_vid = SubscriptionFitnessVideo(
                    user=user,
                    data_start=promo_code_fit_vid.data_start,
                    data_finish=promo_code_fit_vid.data_finish,
                    promo_code=promo_code_fit_vid.code,
                    active=True,
                    sub_type=promo_code_fit_vid.sub_type,
                )
                user_subscription_fit_vid.save()
                attention = f'Ваша подписка оформлена'

        except PromoCodeFitnessVideo.DoesNotExist:
            attention = f'Такого промокода нет 🤪'
        context = {
            'form': SubscriptionFitnessVideoForm(),
            'attention': attention,
        }

    return render(request, 'subscription/subscription_fit_vid_promocode.html', context)


def payment_subscription_fit_vid(request):
    """
    Представление покупки подсписки на график
    """

    if request.method == "POST":
        form_register = RegisterForm(request.POST)
        form_subscription_fitness_video = SubscriptionFitnessVideoForm()

        if form_register.is_valid():
            user = form_register.save()
            user.save()
            raw_password = form_register.cleaned_data.get('password1')
            email = form_register.cleaned_data.get('email')
            user = authenticate(username=user.username, email=email, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form_register = RegisterForm()
    return render(request, 'subscription/pay_subscription.html', {'form': form_register})


class PaymentSubscriptionDetailView(DetailView):
    model = PaymentSubscription
    context_object_name = 'payment_subscription'
    template_name = "subscription/payment_marathon.html"

#
# def register_user_with_subscription(request):
#     """Представление для ручной регистрации пользователя, выдачи подписки и отправки email"""
#     if request.method == "POST":
#         form = AdminRegisterWithSubscriptionForm(request.POST)
#         if form.is_valid():
#             try:
#                 email = form.cleaned_data['email']
#                 sub_type = form.cleaned_data['sub_type']
#
#                 # 1. Генерируем случайный пароль
#                 generated_password = form.generate_random_password()
#
#                 # 2. Создаем пользователя
#                 user = User.objects.create_user(
#                     username=email,
#                     email=email,
#                     password=generated_password
#                 )
#
#                 # 3. Определяем даты подписки
#                 now = timezone.now()
#                 one_year_later = now + timedelta(days=365)
#
#                 # Форматируем дату финиша для письма (например, "03.08.2027")
#                 expire_date_formatted = one_year_later.strftime("%d.%m.%Y")
#
#                 # 4. Создаем подписку
#                 SubscriptionFitnessVideo.objects.create(
#                     user=user,
#                     data_start=now,
#                     data_finish=one_year_later,
#                     active=True,
#                     sub_type=sub_type
#                 )
#
#                 # 5. Запускаем Celery таск на отправку письма в фоне
#                 send_welcome_email_task.delay(
#                     email=email,
#                     password=generated_password,
#                     sub_type=sub_type,
#                     expire_date_str=expire_date_formatted
#                 )
#
#                 messages.success(
#                     request,
#                     f'Пользователь {email} успешно зарегистрирован! '
#                     f'Подписка ({sub_type}) активна до {expire_date_formatted}. '
#                     f'Письмо с паролем отправлено на почту.'
#                 )
#
#                 return redirect('register_with_subscription')
#
#             except Exception as e:
#                 messages.error(request, f"Произошла ошибка: {str(e)}")
#     else:
#         form = AdminRegisterWithSubscriptionForm()
#
#     return render(request, 'authentication/register_with_sub.html', {'form': form})


def register_user_with_subscription(request):
    """Представление для ручной регистрации пользователя, выдачи подписки и отправки email"""
    if request.method == "POST":
        form = AdminRegisterWithSubscriptionForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                sub_type = form.cleaned_data['sub_type']

                # 1. Генерируем случайный пароль
                generated_password = form.generate_random_password()

                # 2. Создаем пользователя
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=generated_password
                )

                # 3. Определяем даты подписки
                now = timezone.now()
                one_year_later = now + timedelta(days=365)
                expire_date_formatted = one_year_later.strftime("%d.%m.%Y")

                # 4. Создаем подписку
                SubscriptionFitnessVideo.objects.create(
                    user=user,
                    data_start=now,
                    data_finish=one_year_later,
                    active=True,
                    sub_type=sub_type
                )

                # 5. Запускаем Celery таск
                send_welcome_email_task.delay(
                    email=email,
                    password=generated_password,
                    sub_type=sub_type,
                    expire_date_str=expire_date_formatted
                )

                # Текст ссылки для экрана админа
                if sub_type == 'type_04':
                    link_text = "Марафон по ссылке: https://simonasoloduha.ru/video/timetable_marathon/"
                elif sub_type == 'type_05':
                    link_text = "Программа по ссылке и на вкладках: ПРОГРАММЫ и ДЛЯ НАЧИНАЮЩИХ: https://simonasoloduha.ru/video/timetable/"
                else:
                    link_text = "Программа по ссылке и на вкладке ПРОГРАММЫ: https://simonasoloduha.ru/video/timetable/"

                # Собираем точную копию текста сообщения
                copy_text = (
                    f"Ваши данные для входа на сайт SIMONA SOLODUHA\n\n\n"
                    f"почта: {email}\n"
                    f"пароль: {generated_password}\n\n\n"
                    f"Страница входа: https://simonasoloduha.ru/auth/login_fitness\n\n"
                    f"{link_text}\n\n"
                    f"Доступ до {expire_date_formatted}\n\n"
                    f"Хороших тренировок и результатов 😘\n\n"
                    f"Если будут вопросы — пишите 🌸"
                )

                # Формируем HTML-уведомление для страницы
                success_html = mark_safe(
                    f"Пользователь <b>{email}</b> успешно зарегистрирован! "
                    f"Подписка (<b>{sub_type}</b>) активна до <b>{expire_date_formatted}</b>.<br>"
                    f"Письмо отправлено на почту.<br><br>"
                    f"<b>Текст письма для копирования:</b>"
                    f"<pre style='background: #f4f4f6; padding: 12px; border-radius: 6px; border: 1px solid #ccc; font-family: monospace; font-size: 13px; margin-top: 8px; user-select: all; white-space: pre-wrap;'>{copy_text}</pre>"
                )

                messages.success(request, success_html)

                return redirect('register_with_subscription')

            except Exception as e:
                messages.error(request, f"Произошла ошибка: {str(e)}")
    else:
        form = AdminRegisterWithSubscriptionForm()

    return render(request, 'authentication/register_with_sub.html', {'form': form})