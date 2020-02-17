#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:53:54 2020

@author: thomas
"""
from bokeh.models import ColumnDataSource, GeoJSONDataSource, HoverTool, Panel, Tabs
from bokeh.palettes import Viridis11
from bokeh.transform import factor_cmap
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets import Button, Select, DataTable, TableColumn, RadioGroup, Div, ColorPicker, Slider
from bokeh.layouts import row, widgetbox, column, Spacer
from bokeh.io import curdoc
import json
import os
import sys
import geopandas as gpd

geodecision_path = os.path.abspath("./geodecision/")

if geodecision_path not in sys.path:
    sys.path.insert(0, geodecision_path)
   
from geodecision import gdf_to_geosource, make_sliders, get_hist_source
from constants import set_para


#####################
# GET PARAMS & DATA #
#####################
#Get json_config from arg
json_config = sys.argv[1]

#Load params JSON file
with open(json_config) as f: 
    params = json.load(f)
values = params["figures_settings"]["values"]
samples = params["figures_settings"]["samples"]
group = params["figures_settings"]["group"]

#Get one gdf
gdfs = []
for layer in params["inputs"]["layers"]:
    gdfs.append(
            gpd.GeoDataFrame.from_file(
                    params["inputs"]["roofs"],
                    layer=layer
                    )
            )
gdf = gpd.pd.concat(gdfs)

#Source for map
# Reprojection to fit with Bokeh tiles
gdf = gdf.to_crs(epsg=3857)

#Manage layers
layers = list(gdf[group].unique())
default = layers[0]

## Transform to GeoJSONDataSource
geo_source = GeoJSONDataSource(
        geojson=gdf_to_geosource(
                gdf.loc[gdf[group] == default]
                )
        )
## Source for Datatable
table_source = ColumnDataSource(
        gdf[
                params["figure_settings"]["table_columns"]
                ].loc[gdf[group] == default]
        )

## Source for accessibility
access = []
for layer in params["inputs"]["accessibility"]["layers"]:
    access.append(
            gpd.GeoDataFrame.from_file(
                    params["inputs"]["accessibility"]["isochrones"],
                    layer=layer
                    )
            )
access = gpd.pd.concat(access)
access = access.to_crs(epsg=3857)

## Background layer
background_source = GeoJSONDataSource(
        geojson=gdf_to_geosource(
                gpd.GeoDataFrame.from_file(params["inputs"]["background"])
                )
        )

## Figure range
x_range = (
        params["figures_settings"]["figure_range"]["x_range"]["left"],
        params["figures_settings"]["figure_range"]["x_range"]["right"]
        )
y_range = (
        params["figures_settings"]["figure_range"]["y_range"]["bottom"],
        params["figures_settings"]["figure_range"]["y_range"]["top"]
        )

#############
# FUNCTIONS #
#############
def update(new):
    button.disabled = True
    tmp = None
    for k,v in sliders.items():
        if v.value is not None:
            start = v.value[0]
            end = v.value[1]
            if tmp is None:
                tmp = gdf.loc[
                        (gdf[k] >= start) 
                        & (gdf[k] < end)
                        ]
            else:
                tmp = tmp.loc[
                        (tmp[k] >= start) 
                        & (tmp[k] < end)
                        ]
    
    if radio_group.active == 1:
        tmp = tmp.loc[tmp["public_access"] == True]
    tmp_map = tmp.loc[tmp[group] == select.value]
    hist_source.data = get_hist_source(tmp, group)
    geo_source.geojson = gdf_to_geosource(tmp_map)
    table_source.data = tmp_map[params["figure_settings"]["table_columns"]]
    button.disabled = False

    para.text = set_para(
            gdf[
                    params["figure_settings"]["table_columns"]
                    ].loc[gdf[group] == select.value],
            tmp_map,
            sliders,
            select.value
            )

def reset(new):
    for slider in sliders.values():
        slider.value = (slider.start, slider.end)
    radio_group.active = 0
        
#######################
# WIDGETS AND FIGURES #
#######################
#Tiles
tile_provider = get_provider(Vendors.STAMEN_TERRAIN)
#Create sliders
sliders = make_sliders(gdf, values, samples=samples)
#Create buttons
button = Button(label="Filter", button_type="success")
reset_button = Button(label="Reset", button_type="warning")
#Create color picker
color_picker = ColorPicker(
        color="#ff4466", 
        title="Choose buildings color:", 
        width=200
        )

#Create select box
select = Select(
        title="Layer:", 
        value=default, 
        options=layers
        )

#HISTOGRAM
#Source for histogram
hist_source = ColumnDataSource(data=get_hist_source(gdf, group)) 
hist = figure(
    x_range=hist_source.data["groups"], 
    plot_height=400, 
    plot_width=600,
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
hist.xaxis.major_label_orientation = 1

#MAP
map_ = figure(
        title="Map",
        output_backend="webgl",
        plot_height=800,
        plot_width=800,
        x_range = x_range,
        y_range = y_range
        )

#Add tile
map_.add_tile(tile_provider)

#Add background
background = map_.patches(
        "xs",
        "ys",
        fill_color = "black",
        fill_alpha = 0.5,
        line_alpha = 0.0,
        source=background_source
        )
## Create linked opacity layer slider
back_slider = Slider(
        start=0, 
        end=1, 
        value=0.5, 
        step=.1, 
        title="Background Opacity"
        )
back_slider.js_link("value", background.glyph, "fill_alpha")

#Add patches
buildings = map_.patches(
        "xs", 
        "ys", 
        fill_color="blue",
        line_color="white",
        fill_alpha = 0.5,
        line_alpha=0.2,
        line_width=0.5,
        source=geo_source
        )

#Link color picker to buildings color glyph
color_picker.js_link("color", buildings.glyph, "fill_color")

#DATATABLE & Tooltips
columns = []
tooltips = []
for col in params["table_columns"]:
    columns.append(
            TableColumn(
                    field=col, 
                    title=col
                    )
            )
    tooltips.append(
            (col, "@" + col)
            )

data_table = DataTable(
        source=table_source, 
        columns=columns,
        height=600,
        width=800
        )

#RADIOGROUP
radio_group = RadioGroup(
        labels=["All buildings", "Only public access buildings"], active=0)

#PARAGRAPH
para = Div(
        text="""""",
        width=600, 
        height=400
        )
para.text = set_para(
            gdf[params["table_columns"]].loc[gdf[group] == select.value],
            gdf.loc[gdf[group] == default],
            sliders,
            select.value
            )

#Widgets
# HOVER TOOL
hover = HoverTool(
        tooltips=tooltips
        )
map_.add_tools(hover)

widgetbox(
        [x for x in sliders.values()]
    )
button.on_click(update)
reset_button.on_click(reset)
widgets = [select, radio_group]
widgets.extend([x for x in sliders.values()])
widgets.extend([button, reset_button])
widgets.extend([color_picker, back_slider])

#Panels and tabs
tab_map = Panel(
        child=map_,
        title="Map"
        )
tab_global = Panel(
        child=column([hist, para]),
        title="Synthesis"
        )
tab_tables = Panel(
        child=data_table,
        title="Datatables"
        )
tabs = Tabs(tabs=[tab_map, tab_tables, tab_global])

#Layout
layout = row(
        widgetbox(widgets),
        Spacer(width=50),
        tabs
        )

#Layout
#layout = row(
#        column(
#                widgetbox(
#                        widgets
#                        )
#                ),
#        column(
#                hist,
#                map_
#                ),
#        column(
#                para,
#                data_table
#                )
#        )

curdoc().add_root(layout)