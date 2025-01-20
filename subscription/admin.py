from django.contrib import admin

from subscription.models import Subscription, SubscriptionFitnessVideo, PromoCodeFitnessVideo, PaymentSubscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'active')


class SubscriptionFitnessVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'active', 'sub_type', 'data_start', 'data_finish', 'phone_number', )


class PromoCodeFitnessVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'data_start', 'data_finish', 'active', 'sub_type', )


class PaymentSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'target', 'description', 'image', 'price_month', 'price_year', 'sale',
                    'price_month_sale', 'price_year_sale', 'active', 'sub_type',)


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionFitnessVideo, SubscriptionFitnessVideoAdmin)
admin.site.register(PromoCodeFitnessVideo, PromoCodeFitnessVideoAdmin)
admin.site.register(PaymentSubscription, PaymentSubscriptionAdmin)
