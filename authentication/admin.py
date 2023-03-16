# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from authentication.models import Code


class CodeAdmin(admin.ModelAdmin):
    """
    Модель кода
    """
    model = Code


admin.site.register(Code, CodeAdmin)
