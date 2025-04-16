from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView

from subscription.models import SubscriptionFitnessVideo, PaymentSubscription
from video.forms import CHOICES_TYPES, CHOICES_BODY_PARTS
from video.models import FitVideo, TIME_CHOICES, Trainer, Timetable


class AllVideos(ListView):
    def get(self, request):
        fit_videos = FitVideo.objects.order_by('-created_at')
        times = list(zip(*TIME_CHOICES))[0]
        types = list(zip(*CHOICES_TYPES))[0]
        body_parts = list(zip(*CHOICES_BODY_PARTS))[0]
        trainer_choices = Trainer.objects.order_by('-first_name')

        context = {
            'fit_videos': fit_videos,
            'trainer_choices': trainer_choices,
            'times': times,
            'types': types,
            'body_parts': body_parts,
        }
        return render(request, 'video/videos.html', context)


class Timetables(ListView):
    def get(self, request):

        payment_subscriptions = PaymentSubscription.objects.all()
        user = request.user
        date = datetime.now()
        if user.is_authenticated:
            try:
                subscription = SubscriptionFitnessVideo.objects.filter(
                    user=user,
                    active=True
                )
                sub_types = subscription.values_list('sub_type', flat=True)

                if sub_types[0] == 'type_00':

                    sub_types_all = ['type_01', 'type_02', 'type_03']
                    timetables = Timetable.objects.filter(sub_bay_type__in=sub_types_all)
                else:
                    timetables = Timetable.objects.filter(sub_bay_type__in=sub_types)

            except SubscriptionFitnessVideo.DoesNotExist:
                timetables = Timetable.objects.none()
        else:
            timetables = Timetable.objects.none()

        context = {
            'timetables': timetables,
            'payment_subscriptions': payment_subscriptions,
        }

        return render(request, 'timetable/timetable.html', context)


class TimetablesMarathon(ListView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                subscription = SubscriptionFitnessVideo.objects.filter(
                    user=user,
                    active=True
                )
                sub_types = subscription.values_list('sub_type', flat=True)

                if 'type_04' in sub_types:
                    timetables = Timetable.objects.filter(sub_bay_type='type_04')
                else:
                    timetables = None

            except SubscriptionFitnessVideo.DoesNotExist:
                timetables = Timetable.objects.none()
        else:
            timetables = Timetable.objects.none()

        context = {
            'timetables': timetables,
        }

        return render(request, 'timetable/timetable_marathon.html', context)
