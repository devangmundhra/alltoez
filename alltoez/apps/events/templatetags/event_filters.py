import logging

from django.utils.dateformat import time_format
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.translation import to_locale, get_language
from django import template

from babel.dates import format_date, format_timedelta

# Get an instance of a logger
logger = logging.getLogger(__name__)
register = template.Library()

@register.filter
def time_range(start_time, end_time):
    """Make time ranges like 7-9 p.m."""
    if start_time is None:
        return u''
    if end_time is None or start_time == end_time:
        return time_format(start_time, 'P')
    if start_time.hour == 12 or start_time.hour == 0 \
       or end_time.hour == 12 or end_time.hour == 0:
        return u'%s - %s' % (time_format(start_time, 'P'), time_format(end_time, 'P'))
    if (start_time.hour < 12 and end_time.hour >= 12) \
       or (end_time.hour < 12 and start_time.hour >= 12):
        return u'%s - %s' % (time_format(start_time, 'P'), time_format(end_time, 'P'))
    first_part = time_format(start_time, 'P')
    first_part = first_part.replace(' a.m.', '').replace(' p.m.', '')
    return u'%s-%s' % (first_part, time_format(end_time, 'P'))

@register.filter
def local_day_date(date_value):
    date = parse_date(date_value)
    return format_date(date, "EEE, MMM d", locale=to_locale(get_language()))

@register.filter
def naturaldatetime(datetime_value):
    datetime = parse_datetime(datetime_value)
    delta = timezone.now().date() - datetime.date()
    return format_timedelta(delta, granularity='day', locale=to_locale(get_language()))