from django import template
from urllib.parse import urlencode
from django.conf import settings

register = template.Library()


@register.filter
def create_range(start: int, end: int, step: int = 1):
    return range(start, end, step)


@register.filter
def format_timedelta(seconds: int | None) -> str:
    print(type(seconds))
    if seconds:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    return "00:00:00"


@register.filter(name='build_qs')
def build_qs(page: str | int, request_GET: dict):
    url_qs = {'page': page}

    for key, value in request_GET.items():
        if key == 'page':
            continue

        if isinstance(value, list):
            url_qs[key] = value[0]
        else:
            url_qs[key] = value

    return "?" + urlencode(url_qs)


@register.filter(name="add_numbers")
def add_numbers(s1, s2):
    return s1 + s2


@register.filter
def is_dict(value):
    return isinstance(value, dict)


@register.filter(name="to_string")
def to_string(value):
    return str(value)


@register.filter(name="language_change_url")
def language_change_url(value, language_code="ka"):
    value = value.lstrip('/')
    for lang in settings.LANGUAGES:
        value = value.lstrip(lang[0] + "/")

    return "/" + value if language_code == "ka" else f"/{language_code}/{value}"
