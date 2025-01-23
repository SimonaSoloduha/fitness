from django.shortcuts import render
from django.http import FileResponse
import os


def dogovor(request):
    filepath = 'static/files/dogovor.pdf'

    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
