from django.urls import path

from dogovor.views import dogovor

urlpatterns = [
    path('', dogovor, name='dogovor'),
]
