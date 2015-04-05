from django import template
#from numpy import log
import numpy as np
from re import match

register = template.Library()

wt_kcat = 840
wt_km = 0.005
wt_eff = 171000

@register.filter(name = 'kcatStyle')
def kcatStyle(value):

    logValue = np.log10( (value/wt_kcat) )
    if logValue < 0:
        if -1 < logValue < 0:
            return "rgb( 150, 205, 205 )"
        elif -2 < logValue < -1:
            return "rgb( 102, 139, 139 )"
        else:
            return "rgb( 47, 79, 79 )"
    elif logValue > 0:
        if 0 < logValue < 1:
            return "rgb( 238, 233, 191 )"
        elif 1 < logValue < 2:
            return "rgb( 238, 220, 130 )"
        else:
            return "rgb( 205, 173, 0 )"
    else:
        return "rgb( 224, 224, 224 )"

@register.filter(name = 'kmStyle')
def kmStyle(value):

    logValue = np.log10( (value/wt_km) )
    if logValue < 0:
        if -1 < logValue < 0:
            return "rgb( 150, 205, 205 )"
        elif -2 < logValue < -1:
            return "rgb( 102, 139, 139 )"
        else:
            return "rgb( 47, 79, 79 )"
    elif logValue > 0:
        if 0 < logValue < 1:
            return "rgb( 238, 233, 191 )"
        elif 1 < logValue < 2:
            return "rgb( 238, 220, 130 )"
        else:
            return "rgb( 205, 173, 0 )"
    else:
        return "rgb( 224, 224, 224 )"

@register.filter(name = 'effStyle')
def effStyle(value):

    logValue = np.log10( (value/wt_eff) )
    if logValue < 0:
        if -1 < logValue < 0:
            return "rgb( 150, 205, 205 )"
        elif -2 < logValue < -1:
            return "rgb( 102, 139, 139 )"
        else:
            return "rgb( 47, 79, 79 )"
    elif logValue > 0:
        if 0 < logValue < 1:
            return "rgb( 238, 233, 191 )"
        elif 1 < logValue < 2:
            return "rgb( 238, 220, 130 )"
        else:
            return "rgb( 205, 173, 0 )"
    else:
        return "rgb( 224, 224, 224 )"

@register.filter(name = 'seq' )
def tr( value ):
    return value[1:-1]
