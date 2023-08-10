from django.shortcuts import render
from subscription.models import Subscription

from subscription.tasks import send_hello_to_email


def subscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # new = Subscription(email=email)
        # new.save()
        send_hello_to_email(email)
    return render(request, 'index.html')
