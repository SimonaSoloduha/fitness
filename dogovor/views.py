from django.shortcuts import render
from django.http import FileResponse
import os


def dogovor(request):
    dogovor_path = '/static/files/dogovor.pdf'
    # basedir = os.path.abspath(os.getcwd())
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    try:
        filepath = os.path.abspath(os.path.join(basedir, dogovor_path))
    except Exception:
        filepath = dogovor_path

    return render(request, 'dogovor/dogovor.html', {'filepath': filepath, 'basedir': basedir})

    # return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
