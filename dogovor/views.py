from django.shortcuts import render
from django.http import FileResponse
import os


def dogovor(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    return render(request, 'dogovor/dogovor.html', {'file_path': current_dir})
