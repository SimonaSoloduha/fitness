from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from subscription.models import Subscription
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
