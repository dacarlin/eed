import math
from django import template
import numpy as np
from re import match

register = template.Library()

color = {
  -3: "rgb( 47, 79, 79 )", 
  -2: "rgb( 102, 139, 139 )", 
  -1: "rgb( 150, 205, 205 )", 
   0: "rgb( 224, 224, 224 )", #neutral
   1: "rgb( 238, 233, 191 )", 
   2: "rgb( 238, 220, 130 )",
   3: "rgb( 238, 220, 130 )", #same as -2 for now 

}

def colorize( value, arg ):
  result = math.floor( np.log( value / arg ) )  
  if -3 <= result <= 3:
    return color[ result ]
  else:
    return 'rgba( 0, 0, 0, 0 )' 

def cut( value ):
  return filter( unicode.isdigit, value ) #hack that will only work for single mutants 

register.filter( 'colorize', colorize ) 
register.filter( 'compare_to', colorize ) 
register.filter( 'cut', cut ) 
