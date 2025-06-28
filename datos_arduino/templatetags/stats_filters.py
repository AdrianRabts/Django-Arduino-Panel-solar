from django import template

register = template.Library()

@register.filter
def max_val(queryset, field):
    return max(getattr(x, field) for x in queryset) if queryset else ''

@register.filter
def min_val(queryset, field):
    return min(getattr(x, field) for x in queryset) if queryset else ''

@register.filter
def average_val(queryset, field):
    vals = [getattr(x, field) for x in queryset]
    return round(sum(vals)/len(vals), 1) if vals else ''
