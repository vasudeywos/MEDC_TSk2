from django import template

register = template.Library()

@register.filter
def get_count(dictionary, key):
    return dictionary.get(key, 0)
