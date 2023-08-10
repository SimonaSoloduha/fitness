from django import template

from subscription.forms import SubscriptionForm

register = template.Library()


@register.inclusion_tag("subscription/tags/subscription_form.html")
def subscription_form():
    return {'subscription_form': SubscriptionForm()}
