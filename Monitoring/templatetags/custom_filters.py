from django import template
register = template.Library()
# В custom_filters.py

@register.filter
def abs_val(value):
    return abs(int(value))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
