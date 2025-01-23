from django.shortcuts import render
from django.http import FileResponse
import os


def dogovor(request):
    dogovor_path = '/static/files/dogovor.pdf'
    basedir = os.path.abspath(os.getcwd())
    filepath = os.path.abspath(os.path.join(basedir, dogovor_path))

    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
