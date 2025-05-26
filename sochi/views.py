from django.shortcuts import render

# Create your views here.


def sochi(request):
    """
    Представление тренировок в Сочи
    """

    return render(request, 'sochi/sochi_index.html')
