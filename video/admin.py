from django.contrib import admin

from video.forms import FitVideoForm, TimetableForm
from video.models import FitVideo, Trainer, Timetable


class FitVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'trainer')
    form = FitVideoForm


class TrainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name')


class TimetableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sub_bay_type',)

    form = TimetableForm


admin.site.register(FitVideo, FitVideoAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Timetable, TimetableAdmin)
