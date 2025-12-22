"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from fitness import views, settings

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls'), name='authentication'),
    path('video/', include('video.urls'), name='video'),
    path('sochi/', include('sochi.urls'), name='sochi'),
    path('', include('subscription.urls')),
    path('zen_8oRVPGRA4zgBaqFz0nUn4AoUUrQEOHxjnEoq3wd5gm2SGlha55ANlTxhZGXApyoL.html', views.dzen, name='dzen'),
    path('https://simonasoloduha.ru/yandex_cd02769b2d0a6efd.html ', views.yandex,
                       name='yandex'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
