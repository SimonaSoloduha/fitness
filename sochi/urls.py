from django.urls import path

from sochi.views import sochi

urlpatterns = [
    path('sochi/', sochi, name='sochi_info'),
]
