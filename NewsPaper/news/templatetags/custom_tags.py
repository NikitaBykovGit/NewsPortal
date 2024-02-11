from django import template
from django.utils import timezone

import pytz

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag()
def current_time():
    return timezone.localtime(timezone.now())


@register.simple_tag()
def timezones():
    return pytz.common_timezones