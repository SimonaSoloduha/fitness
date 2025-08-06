from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True

TYPE_CHOICES = [
    ('type_00', 'type_00'),
    ('type_01', 'type_01'),
    ('type_02', 'type_02'),
    ('type_03', 'type_03'),
    ('type_04', 'type_04'),
    ('type_05', 'type_05'),
    ('type_06', 'type_06'),

]


class Subscription(models.Model):
    """ Модель подписки email"""
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'), blank=True)
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

    # def save(self, *args, **kwargs):
    #     self.validate_unique()
    #     super(SubscriptionFitnessVideo, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.sub_type} - {self.active}'


class PromoCodeFitnessVideo(models.Model):
    """ Модель промокода подписки на видео """
    code = models.CharField(blank=True, null=True, max_length=12, verbose_name=_('code'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    data_start = models.DateTimeField(verbose_name=_('data_start'))
    data_finish = models.DateTimeField(verbose_name=_('data_finish'))
    active = models.BooleanField(default=False, verbose_name=_('active'))
    sub_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name=_('sub_type'),
        blank=True,
    )

    class Meta:
        verbose_name_plural = _('promo_code_fit_video')
        verbose_name = _('promo_code_fit_videos')

    def __str__(self):
        return f'{self.code}'


class PaymentSubscription(models.Model):
    """ Модель абониимента """
    name = models.CharField(blank=True, null=True, max_length=25, verbose_name=_('name'))
    level = models.CharField(blank=True, max_length=200, verbose_name=_('level'))
    schedule = models.CharField(blank=True, max_length=200, verbose_name=_('schedule'))
    for_whom = models.CharField(blank=True, max_length=300, verbose_name=_('for_whom'))
    result = models.CharField(blank=True, max_length=300, verbose_name=_('result'))
    target = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('target'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    image = models.ImageField(upload_to='payment_subscription_img', blank=True, null=True, height_field=None,
                              width_field=None, max_length=100)
    price_month = models.DecimalField(max_digits=6, decimal_places=0, verbose_name=_('price_month'))
    price_year = models.DecimalField(max_digits=6, decimal_places=0, verbose_name=_('price_year'))
    sale = models.DecimalField(max_digits=6, decimal_places=0, null=True, verbose_name=_('sale'))
    price_month_sale = models.DecimalField(max_digits=6, decimal_places=0, verbose_name=_('price_month_sale'))
    price_year_sale = models.DecimalField(max_digits=6, decimal_places=0, verbose_name=_('price_year_sale'))
    url_pay_month = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('url_pay_month'))
    url_pay_year = models.CharField(blank=True, null=True, max_length=100, verbose_name=_('url_pay_year'))
    active = models.BooleanField(default=False, verbose_name=_('active'))
    sub_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name=_('sub_type'),
        blank=True,
    )

    class Meta:
        verbose_name_plural = _('payment_subscription')
        verbose_name = _('payment_subscriptions')

    def __str__(self):
        return f'{self.name}'
