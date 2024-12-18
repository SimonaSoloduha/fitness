from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from subscription.models import SubscriptionFitnessVideo
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

        user = request.user

        try:
            subscription = SubscriptionFitnessVideo.objects.get(user=user)
            timetables = Timetable.objects.filter(sub_bay_type__contains=subscription.sub_type)
        except SubscriptionFitnessVideo.DoesNotExist:
            timetables = Timetable.objects.none()

        context = {
            'timetables': timetables,
        }

        return render(request, 'timetable/timetable.html', context)
