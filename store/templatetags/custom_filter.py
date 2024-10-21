from django import template

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
