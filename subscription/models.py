from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True

TYPE_CHOICES = [
    ('type_00', 'type_00'),
    ('type_01', 'type_01'),
    ('type_02', 'type_02'),
    ('type_03', 'type_03'),
]


class Subscription(models.Model):
    """ Модель подписки """
    email = models.EmailField(unique=True, verbose_name=_('email'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    active = models.BooleanField(default=True, verbose_name=_('active'))

    class Meta:
        verbose_name_plural = _('subscription')
        verbose_name = _('subscriptions')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class SubscriptionFitnessVideo(models.Model):
    """ Модель подписки на видео """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    data_start = models.DateTimeField(verbose_name=_('data_start'))
    data_finish = models.DateTimeField(verbose_name=_('data_finish'))
    promo_code = models.TextField(blank=True, verbose_name=_('promo_code'))
    active = models.BooleanField(default=False, verbose_name=_('active'))
    sub_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name=_('sub_type'),
        blank=True,
    )
    phone_number = models.CharField(blank=True, null=True, max_length=12, verbose_name=_('phone_number'))

    class Meta:
        verbose_name_plural = _('subscription_fit_video')
        verbose_name = _('subscription_fit_videos')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(SubscriptionFitnessVideo, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.sub_type} - {self.active}'
