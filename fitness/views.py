# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from subscription.models import PaymentSubscription
from video.models import Trainer, Timetable


def index(request):
    trainers = Trainer.objects.order_by('-first_name')
    payment_subscriptions = PaymentSubscription.objects.all()
    # timetables = Timetable.objects.order_by('-created_at')

    context = {
        'trainers': trainers,
        'payment_subscriptions': payment_subscriptions,
        # 'timetables': timetables,
    }
    return render(request, 'index.html', context)
