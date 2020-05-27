from django import template

register = template.Library()


@register.filter
def inc(arg1, arg2):
    return int(arg1) + int(arg2)


@register.simple_tag
def division(arg1, arg2, to_int=False):
    if to_int:
        return int(int(arg1) / int(arg2))
    return float(arg1) / float(arg2)
