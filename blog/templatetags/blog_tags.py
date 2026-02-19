import re
from django import template

register = template.Library()


@register.filter
def strip_tags(value):
    return re.sub(r'<[^>]+>', '', value)


@register.filter
def reading_time(body):
    word_count = len(re.sub(r'<[^>]+>', '', body).split())
    return max(1, round(word_count / 200))
