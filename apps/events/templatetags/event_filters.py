import logging

from django.utils.dateformat import time_format
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.translation import to_locale, get_language
from django import template
from django.template.defaultfilters import stringfilter

from babel.dates import format_date, format_timedelta

# Get an instance of a logger
logger = logging.getLogger(__name__)
register = template.Library()


@register.filter(expects_localtime=True)
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
def get_datetime_date(date_value):
    date = parse_date(date_value)
    return date


@register.filter
def format_date_filter(date_value, format_type='medium'):
    date = parse_date(date_value)
    return format_date(date, format=format_type, locale=to_locale(get_language()))


@register.filter
def naturaldatetime(datetime_value):
    datetime = parse_datetime(datetime_value)
    delta = timezone.now().date() - datetime.date()
    return format_timedelta(delta, granularity='day', locale=to_locale(get_language()))


@register.filter
def days_since(datetime_value):
    datetime = parse_datetime(datetime_value)
    delta = timezone.now().date() - datetime.date()
    return delta.days


@register.filter
@stringfilter
def format_event_datetime(value):
    """
    Convert the event datetime into GFM format of tables
    https://help.github.com/articles/github-flavored-markdown/#tables
    :param value: event days and time persisted in the db
    :return: tabular format of event days and time
    """
    if value.find(': ') == -1:
        # No point converting this into table form since this is not in the Days: Time format
        return value
    split_string = '\r\n'
    value = value.replace(split_string+split_string, split_string)
    in_lines = value.split(split_string)
    out_lines = ['|', '-|-']
    for line in in_lines:
        split_line = line.split(': ')
        if len(split_line) == 1:
            out_lines.append('{}|'.format(split_line[0]))
        else:
            out_lines.append('|'.join(split_line))

    output = split_string.join(out_lines)
    return output


@register.filter
@stringfilter
def format_event_cost(value):
    """
    Convert the event cost into GFM format of tables
    https://help.github.com/articles/github-flavored-markdown/#tables
    :param value: cost info persisted in the db
    :return: tabular format of event days and time
    """
    if value.find(', ') == -1:
        # No point converting this into table form since this is not in the Cost, (Attr) format
        return value
    split_string = ', '
    in_lines = value.split(split_string)
    out_lines = ['|', '-|-']
    for line in in_lines:
        split_line = line.split(' (')
        print split_line
        if len(split_line) == 1:
            out_lines.append('{}|'.format(split_line[0]))
        else:
            out_lines.append('{}|{}'.format(split_line[1], split_line[0]))

    output = '\r\n'.join(out_lines)
    output = output.replace(')', '')
    return output