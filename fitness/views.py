# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from subscription.models import PaymentSubscription, SubscriptionFitnessVideo
from video.models import Trainer, Timetable


def index(request):
    trainers = Trainer.objects.order_by('-first_name')
    payment_subscriptions = PaymentSubscription.objects.all()
    # user = request.user
    # user_marathon_true = False
    # # date = datetime.now()
    # if user.is_authenticated:
    #     try:
    #         subscription = SubscriptionFitnessVideo.objects.filter(
    #             user=user,
    #             active=True
    #         )
    #         sub_types = subscription.values_list('sub_type', flat=True)
    #
    #         if 'type_04' in sub_types:
    #             timetables = Timetable.objects.filter(sub_bay_type='type_04')
    #             if timetables:
    #                 user_marathon_true = True
    #     except SubscriptionFitnessVideo.DoesNotExist:
    #         user_marathon_true = False

    context = {
        'trainers': trainers,
        'payment_subscriptions': payment_subscriptions,
        # 'user_marathon_true': user_marathon_true,
    }

    # print('user_marathon_true', user_marathon_true)
    return render(request, 'index.html', context)
