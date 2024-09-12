from django.contrib import admin

from subscription.models import Subscription, SubscriptionFitnessVideo


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'active')


class SubscriptionFitnessVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'active', 'sub_type', 'data_start', 'data_finish', 'phone_number', )


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionFitnessVideo, SubscriptionFitnessVideoAdmin)
