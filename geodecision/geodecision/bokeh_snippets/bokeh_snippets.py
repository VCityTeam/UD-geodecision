#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:54:20 2020

@author: thomas
"""
from bokeh.models.widgets import RangeSlider
import numpy as np


def _set_step(start, end, samples=100):
    """
    Description
    ------------
    
    Set step based on np.linspace
    
    Returns
    --------
    
    Step value
    
    Parameters
    -----------
    
    - start(real)
    - end(real)
    - samples(int):
        - default: 100
    """    
    
    array = np.linspace(start, end, samples)
    
    return array[1]-array[0]

def make_sliders(gdf, values, samples):
    """
    Description
    ------------
    
    Set RangeSliders for a list of values from a (Geo)DataFrame
    
    Returns
    --------
    
    Dict of Bokeh RangeSliders
    
    Parameters
    -----------
    
    - gdf(GeoDataFrame o DataFrame):
        - GeoPandas GeoDataFrame or Pandas DataFrame
    - values(list):
        - list of values for which RangeSlider is needed
    - steps(int):
        - number of samples for steps 
        (used to determine step, based on _set_step())
    """     
    sliders = {}
    roofs_related = ["angles", "area", "min_width", "compactness"]
    for value in values:
        start = gdf[value].min()
        end = gdf[value].max()
        step = _set_step(start, end, samples)
        if value in roofs_related:
            title = value + " (Roof's polygon)"
        elif value == "total_surface":
            title = "total surface (ground area * nb levels)"
        else:
            title = value + " (Building)"
        sliders[value] = RangeSlider(
            start = gdf[value].min(),
            end = gdf[value].max(),
            step=step,
            title = title,
            value=(
                gdf[value].min(),
                gdf[value].max()
            )
        )
            
    return sliders
        
def get_hist_source(gdf, group):
    """
    Description
    ------------
    
    Set and format dict for Bokeh ColumnDataSource for histograms 
    Based on a (Geo)DataFrame groupby
    
    Returns
    --------
    Dict of groups and sums by group
    
    Parameters
    -----------
    
    - gdf(GeoDataFrame or DataFrame):
        - GeoPandas GeoDataFrame or Pandas DataFrame
    - group(str):
        - value to groupby
    """     
    groups = gdf[group].unique()
    groupby = gdf.groupby(group)
    sums = [len(groupby.get_group(group)) for group in groups]
    
    return dict(
        groups = groups,
        sums = sums
    )
