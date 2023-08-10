# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True


def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))


class Code(models.Model):
    """ Модель кода подтверждения через email """
    number = models.CharField(max_length=5, blank=True, verbose_name=_('number'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))

    class Meta:
        verbose_name_plural = _('code')
        verbose_name = _('codes')

    def save(self, *args, **kwargs):
        code = generate_code()
        self.number = code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number
