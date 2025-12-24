# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pathlib import Path
from django.http import FileResponse, Http404
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from subscription.models import PaymentSubscription
from video.models import Trainer


def index(request):
    trainers = Trainer.objects.order_by('-first_name')
    payment_subscriptions = PaymentSubscription.objects.all()
    # user = request.user
    # user_marathon_true = False
    # # date = datetime.now()
    # if user.is_authenticated:
    #     try:
    #         subscription = SubscriptionFitnessVideo.objects.filter(
    #             user=user,
    #             active=True
    #         )
    #         sub_types = subscription.values_list('sub_type', flat=True)
    #
    #         if 'type_04' in sub_types:
    #             timetables = Timetable.objects.filter(sub_bay_type='type_04')
    #             if timetables:
    #                 user_marathon_true = True
    #     except SubscriptionFitnessVideo.DoesNotExist:
    #         user_marathon_true = False

    context = {
        'trainers': trainers,
        'payment_subscriptions': payment_subscriptions,
        # 'user_marathon_true': user_marathon_true,
    }

    # print('user_marathon_true', user_marathon_true)
    return render(request, 'index.html', context)


@xframe_options_exempt
def advertising(request):
    """
    Показываем PDF во встроенном viewer + кнопка «На главную».
    """
    path_to_pdf_file = Path(settings.BASE_DIR) / 'templates' / 'advertising' / 'SimonaSoloduhaMediaKit.pdf'
    if not path_to_pdf_file.exists():
        raise Http404('PDF not found')

    # имя файла для встроенного показа (браузер сам вызовет второй запрос)
    pdf_url = request.build_absolute_uri()  # текущий URL – туда же, но без ?embed
    if request.GET.get('embed') == '1':
        # второй заход: "?embed=1" – отдаём сам PDF
        return FileResponse(open(path_to_pdf_file, 'rb'), content_type='application/pdf')

    # первый заход – возвращаем HTML-обёртку
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Media-kit – Simona Soloduha</title>
    <style>
        *{{box-sizing:border-box;margin:0;padding:0}}
        body{{font-family:Arial,Helvetica,sans-serif;background:#f5f5f5}}
        .bar{{
            position:fixed;top:0;left:0;right:0;
            height:56px;background:#01000d;display:flex;
            align-items:center;padding:0 1rem;z-index:1000;box-shadow:0 2px 8px rgba(0,0,0,.35)
        }}
        .bar a{{
            color:#fff;text-decoration:none;font-size:1rem;
            border:1px solid #6dc0ef;padding:6px 14px;border-radius:4px;
            transition:background .25s
        }}
        .bar a:hover{{background:#6dc0ef}}
        #viewer{{
            position:fixed;top:56px;left:0;right:0;bottom:0;width:100%;height:calc(100vh - 56px);
            border:none
        }}
    </style>
</head>
<body>
    <div class="bar">
        <a href="/">← На главную</a>
    </div>
    <iframe id="viewer" src="{pdf_url}?embed=1"></iframe>
</body>
</html>"""
    return HttpResponse(html)


def dzen(request):
    return render(request, 'dzen.html')


def yandex(request):
    return render(request, 'yandex_cd02769b2d0a6efd.html')
