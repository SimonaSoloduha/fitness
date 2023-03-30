from django.urls import path

from video.views import AllVideos

urlpatterns = [
    path('', AllVideos.as_view(), name='all'),
]
