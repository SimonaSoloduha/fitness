from django.shortcuts import render
from django.http import FileResponse
import os


def dogovor(request):
    dogovor_path = 'static/files/dogovor.pdf'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        file_path = os.path.join(current_dir, dogovor_path)
    except Exception:
        file_path = current_dir
    return render(request, 'dogovor/dogovor.html', {'file_path': file_path})

    # return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
