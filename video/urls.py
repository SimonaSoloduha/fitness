from django.urls import path

from video.views import AllVideos, Timetables

urlpatterns = [
    path('', AllVideos.as_view(), name='all'),
    path('timetable/', Timetables.as_view(), name='timetable'),
]
