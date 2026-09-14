from django.urls import path

from video.views import AllVideos, Timetables, TimetablesMarathon, TimetablesBeginner, payment_subscription_payment

urlpatterns = [
    path('', AllVideos.as_view(), name='all'),
    path('timetable/', Timetables.as_view(), name='timetable'),
    path(
        'timetable/payment/<slug:pk>/',
        payment_subscription_payment,
        name='payment_subscription_payment'
    ),
    path('timetable_marathon/', TimetablesMarathon.as_view(), name='timetable_marathon'),
    path('timetable_beginner/', TimetablesBeginner.as_view(), name='timetable_beginner'),
]
