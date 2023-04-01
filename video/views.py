from django.shortcuts import render
from django.views.generic import ListView

from video.forms import CHOICES_TYPES, CHOICES_BODY_PARTS
from video.models import FitVideo, TIME_CHOICES, Trainer


class AllVideos(ListView):
    def get(self, request):
        fit_videos = FitVideo.objects.order_by('-created_at')
        times = list(zip(*TIME_CHOICES))[0]
        types = list(zip(*CHOICES_TYPES))[0]
        body_parts = list(zip(*CHOICES_BODY_PARTS))[0]
        trainer_choices = Trainer.objects.order_by('-')

        context = {
            'fit_videos': fit_videos,
            'trainer_choices': trainer_choices,
            'times': times,
            'types': types,
            'body_parts': body_parts,
        }
        return render(request, 'video/videos.html', context)
