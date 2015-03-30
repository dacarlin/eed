from django import template
from math import log
from re import match

register = template.Library()

# to determine how transparent to make the values, first decide if the value is
# greater than the wild type.
# if it is larger, divide the wild type by the value and subtract that from one. The
# values furthest from the wild type will be darker (yellow)
# if it is smaller, then subtract that percentage from one and the
# values furthest from the wild type will be darker (blue)

@register.filter(name = 'kcatStyle')
def kcatStyle(value):
    if value > 840:
        a = 1 - (840/value)
        return "rgba( 255, 255, 0, %.2f )" % a
    else:
        a = 1 - (value/840)
        return "rgba( 0, 0, 255, %.2f )" % a

@register.filter(name = 'kmStyle')
def kmStyle(value):
    if value > 0.005:
        a = 1 - value
        return "rgba( 255, 255, 0, %.2f )" % a
    else:
        a = 1 - (value/0.005)
        return "rgba( 0, 0, 255, %.2f )" % a

@register.filter(name = 'effStyle')
def effStyle(value):
    if value > 171000:
        a = 1 - (171000/value)
        return "rgba( 255, 255, 0, %.2f )" % a
    else:
        a = 1 - (value/171000)
        return "rgba( 0, 0, 255, %.2f )" % a

@register.filter(name = 'seq' )
def tr( value ):
    return value[1:-1]