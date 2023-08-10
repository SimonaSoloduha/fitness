from django.contrib import admin

from subscription.models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'active')


admin.site.register(Subscription, SubscriptionAdmin)
