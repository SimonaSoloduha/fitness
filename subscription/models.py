from django.db import models
from django.utils.translation import gettext_lazy as _


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
