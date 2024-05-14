import ast

from django.db import models

from embed_video.fields import EmbedVideoField
from django.utils.translation import gettext_lazy as _


TIME_CHOICES = [
    ('5', 5),
    ('10', 10),
    ('15', 15),
    ('20', 20),
    ('25', 25),
    ('30', 30),
    ('35', 35),
    ('40', 40),
    ('45', 45),
    ('50', 50),
    ('55', 55),
    ('60', 60),
]


class Trainer(models.Model):
    """ Модель тренера """
    first_name = models.CharField(max_length=200, verbose_name=_('first_name'), blank=True)
    last_name = models.CharField(max_length=200, verbose_name=_('last_name'), blank=True)
    about = models.TextField(blank=True, verbose_name=_('about'))
    foto = models.ImageField(upload_to='trainers', height_field=None, width_field=None, max_length=100,
                             blank=True)

    class Meta:
        verbose_name_plural = _('Trainers')

    def __str__(self):
        return f'{self.last_name}'


class FitVideo(models.Model):
    """ Модель видео """
    name = models.CharField(max_length=200, verbose_name=_('name'))
    about = models.TextField(blank=True, verbose_name=_('about'))
    image = models.ImageField(upload_to='video_img', blank=True, null=True, height_field=None, width_field=None, max_length=100)
    video = EmbedVideoField(verbose_name=_('video'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    types = models.CharField(max_length=200, blank=True, verbose_name=_('types'))
    body_parts = models.CharField(max_length=200, blank=True, verbose_name=_('body_parts'))
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, verbose_name=_('trainer'),
                                related_name='trainer')
    free = models.BooleanField(default=True, verbose_name=_('free'))
    times = models.CharField(
        max_length=2,
        choices=TIME_CHOICES,
        verbose_name=_('times'),
        blank=True,
    )

    class Meta:
        verbose_name_plural = _('FitVideos')

    def __str__(self):
        return f'№ {self.id}  {self.name}'

    def convert_to_list(self, data):
        return ast.literal_eval(data)

    def save(self, *args, **kwargs):
        self.types = ' '.join(self.convert_to_list(self.types))
        self.body_parts = ' '.join(self.convert_to_list(self.body_parts))
        super(FitVideo, self).save(*args, **kwargs)


class Timetable(models.Model):
    """ Модель недели расписания """
    name = models.CharField(max_length=200, verbose_name=_('name'))
    about = models.TextField(blank=True, verbose_name=_('about'))
    free = models.BooleanField(default=True, verbose_name=_('free'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    mo_morning = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('mo_morning'), related_name='mo_morning')
    mo_evening = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('mo_evening'), related_name='mo_evening')
    to_morning = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('to_morning'), related_name='to_morning')
    to_evening = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('to_evening'), related_name='to_evening')
    we_morning = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('we_morning'), related_name='we_morning')
    we_evening = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('we_evening'), related_name='we_evening')
    th_morning = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('th_morning'), related_name='th_morning')
    th_evening = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('th_evening'), related_name='th_evening')
    fr_morning = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('fr_morning'), related_name='fr_morning')
    fr_evening = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('fr_evening'), related_name='fr_evening')
    sa_morning = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('sa_morning'), related_name='sa_morning')
    sa_evening = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('sa_evening'), related_name='sa_evening')
    su_morning = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('su_morning'), related_name='su_morning')
    su_evening = models.ManyToManyField(FitVideo, blank=True, verbose_name=_('su_evening'), related_name='su_evening')

    class Meta:
        verbose_name_plural = _('Timetables')

    def __str__(self):
        return f'{self.name}'
