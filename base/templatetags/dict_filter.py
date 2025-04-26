from django import template

register = template.Library()


@register.filter
def dict_filter(dictionary: dict, key: any) -> any:
    return dictionary.get(key, [])
