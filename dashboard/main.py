#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:53:54 2020

@author: thomas
"""
from bokeh.models import ColumnDataSource, GeoJSONDataSource
from bokeh.palettes import Viridis11
from bokeh.transform import factor_cmap
from bokeh.plotting import figure, output_notebook, show
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets import RangeSlider, Button
from bokeh.layouts import row, widgetbox
from bokeh.io import curdoc
import json
import numpy as np
import os
import sys
import geopandas as gpd

geodecision_path = os.path.abspath("./geodecision/")

if geodecision_path not in sys.path:
    sys.path.insert(0, geodecision_path)
   
from geodecision import gdf_to_geosource, make_sliders, get_hist_source

#Get file and GeoDataFrame
json_config = sys.argv[1]

#Load params JSON file
with open(json_config) as f: 
    params = json.load(f)

#Get one gdf
gdfs = []
for layer in params["layers"]:
    gdfs.append(gpd.GeoDataFrame.from_file(params["gdf"], layer=layer))
gdf = gpd.pd.concat(gdfs)
values = params["values"]
samples = params["samples"]
group = params["group"]


#######################
# WIDGETS AND FIGURES #
#######################

#Create sliders
sliders = make_sliders(gdf, values, samples=samples)

#Create Button
button = Button(label="Filter", button_type="success")

#Source for histogram
hist_source = ColumnDataSource(data=get_hist_source(gdf, group)) 

#Histogram
hist = figure(
    x_range=hist_source.data["groups"], 
    plot_height=350, 
    toolbar_location=None, 
    title="Sums by place"
)

hist.vbar(x="groups", 
       top="sums", 
       width=0.9, 
       source=hist_source, 
       legend_field="sums",
       line_color='white', 
       fill_color=factor_cmap(
           "groups", 
           palette=Viridis11, 
           factors=hist_source.data["groups"]
       )
      )
hist.xgrid.grid_line_color = None
hist.legend.orientation = "horizontal"
hist.legend.location = "top_center"

def update(new):
    for k,v in sliders.items():
        if v.value is not None:
            start = v.value[0]
            end = v.value[1]
            tmp = gdf.loc[
                    (gdf[k] >= start) 
                    & (gdf[k] < end)
                    ]
            hist_source.data = get_hist_source(tmp, group)

widgetbox(
        [x for x in sliders.values()]
    )

button.on_click(update)
widgets = [x for x in sliders.values()]
widgets.append(button)

layout = row(
    hist,
    widgetbox(
        widgets
    )
)

curdoc().add_root(layout)