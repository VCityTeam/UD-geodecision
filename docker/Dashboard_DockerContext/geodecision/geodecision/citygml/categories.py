#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
categories

@author: Thomas Leysens
"""

from bokeh.palettes import Viridis4, Magma4, Plasma4


def get_dict_color(choice="viridis"):
    palette = []
    if choice == "viridis":
        colors = Viridis4
    elif choice == "magma":
        colors = Magma4
    elif choice == "plasma":
        colors = Plasma4
        
    for color in colors:
        palette.append(color)
    
    palette.append("red") #for undefined
    
    dict_color = {
    "0 <= x <= 1":palette[0],
    "1 < x <= 5":palette[1],
    "5 < x <= 30":palette[2],
    "30 < x":palette[3],
    "undefined":palette[4]
    }
    
    return dict_color

#Make categories
def make_cat(x):
    if x >= 0.0 and x <= 1.0:
        cat = "0 <= x <= 1"
    elif x > 1.0 and x <= 5.0:
        cat = "1 < x <= 5"
    elif x > 5.0 and x <= 30.0:
        cat = "5 < x <= 30"
    elif x > 30.0 and x <=180:
        cat = "30 < x"
    else:
        cat = "undefined"
        
    return cat