from django import forms

from video.models import FitVideo

CHOICES_TYPES = [
    ('cardio', 'кардио'),
    ('box', 'бокс'),
    ('barre', 'танцы'),
    ('dumbbells', 'гантели'),
    ('floor', 'на коврике'),
    ('gum', 'резинка'),
    ('power', 'силовые'),
]

CHOICES_BODY_PARTS = [
    ('legs', 'ноги'),
    ('butt', 'ягодицы'),
    ('arms', 'руки'),
    ('shoulders', 'плечи'),
    ('abs', 'пресс'),
]


class FitVideoForm(forms.ModelForm):
    types = forms.MultipleChoiceField(choices=CHOICES_TYPES)
    body_parts = forms.MultipleChoiceField(choices=CHOICES_BODY_PARTS)

    class Meta:
        model = FitVideo
        fields = ['name', 'about', 'image', 'video', 'types', 'body_parts', 'trainer', 'times']
