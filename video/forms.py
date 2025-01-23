from django import forms
from django.utils.translation import gettext_lazy as _

from video.models import FitVideo, Timetable

CHOICES_TYPES = [
    (_('cardio'), 'кардио'),
    (_('box'), 'бокс'),
    (_('barre'), 'танцы'),
    (_('dumbbells'), 'гантели'),
    (_('floor'), 'на коврике'),
    (_('gum'), 'резинка'),
    (_('power'), 'силовые'),
]

CHOICES_BODY_PARTS = [
    (_('legs'), 'ноги'),
    (_('butt'), 'ягодицы'),
    (_('arms'), 'руки'),
    (_('shoulders'), 'плечи'),
    (_('abs'), 'пресс'),
    (_('all'), 'все тело'),
]


SUBSCRIPTIONS_BAY_TYPES = [
    ('type_00', 'type_00'),
    ('type_01', 'type_01'),
    ('type_02', 'type_02'),
    ('type_03', 'type_03'),
]


class FitVideoForm(forms.ModelForm):
    types = forms.MultipleChoiceField(choices=CHOICES_TYPES)
    body_parts = forms.MultipleChoiceField(choices=CHOICES_BODY_PARTS)

    class Meta:
        model = FitVideo
        fields = ['name', 'image', 'url_youtube', 'url_rutube', 'url_vk', 'types', 'body_parts', 'trainer',
                  'times']


class TimetableForm(forms.ModelForm):
    sub_bay_type = forms.MultipleChoiceField(choices=SUBSCRIPTIONS_BAY_TYPES)

    class Meta:
        model = Timetable
        fields = ['name', 'about', 'free', 'sub_bay_type', 'mo', 'to', 'we', 'th', 'fr', 'sa', 'su']
