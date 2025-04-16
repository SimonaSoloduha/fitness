from django.urls import path

from video.views import AllVideos, Timetables, TimetablesMarathon

urlpatterns = [
    path('', AllVideos.as_view(), name='all'),
    path('timetable/', Timetables.as_view(), name='timetable'),
    path('timetable_marathon/', TimetablesMarathon.as_view(), name='timetable_marathon'),
]
