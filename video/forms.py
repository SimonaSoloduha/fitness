from django import forms
from django.utils.translation import gettext_lazy as _

from video.models import FitVideo

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
]


class FitVideoForm(forms.ModelForm):
    types = forms.MultipleChoiceField(choices=CHOICES_TYPES)
    body_parts = forms.MultipleChoiceField(choices=CHOICES_BODY_PARTS)

    class Meta:
        model = FitVideo
        fields = ['name', 'about', 'image', 'video', 'types', 'body_parts', 'trainer', 'times']
