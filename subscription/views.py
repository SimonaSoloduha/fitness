from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from authentication.forms import RegisterForm
from subscription.forms import SubscriptionFitnessVideoForm
from subscription.models import Subscription, SubscriptionFitnessVideo, PromoCodeFitnessVideo
from subscription.tasks import send_hello_to_email


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