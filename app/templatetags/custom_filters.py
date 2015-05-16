import math
from django import template
import numpy as np
from re import match

register = template.Library()

color = {

  -4: "rgb( 47, 79, 79 )", #same as -3 for now 
  -3: "rgb( 47, 79, 79 )", 
  -2: "rgb( 102, 139, 139 )", 
  -1: "rgb( 150, 205, 205 )", 
   0: "rgb( 224, 224, 224 )", #neutral
   1: "rgb( 238, 233, 191 )", 
   2: "rgb( 238, 220, 130 )",
   3: "rgb( 238, 220, 130 )", #same as -2 for now 
   4: "rgb( 238, 220, 130 )", 

}

def colorize( value, arg ):
  if value == None: # it's missing  
    return 'rgba( 0,0,0,0 )'
  else:
    result = math.floor( np.log( value / arg ) )  
    if result <= -4:
      return "rgba( 47, 79, 79, 1 )"
    elif result >= 4:
      return "rgb( 238, 220, 130 )"
    elif -4 <= result <= 4:
      return color[ result ]
    else:
      return 'rgba( 255, 0, 0, 0.2 )' #outside dyanamic range!

def cut( value ):
  return filter( unicode.isdigit, value ) #hack that will only work for single mutants 

register.filter( 'colorize', colorize ) 
register.filter( 'compare_to', colorize ) 
register.filter( 'cut', cut ) 
