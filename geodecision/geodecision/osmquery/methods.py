#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 11:50:32 2019

@author: thomas
"""

#import overpass
import osmnx as ox
import geojson
import json
import geopandas as gpd

from ..graph.utils import islist

#def get_OSM_poly(
#        bbox, 
#        key, 
#        value="all", 
#        timeout=40,
#        endpoint="https://overpass-api.de/api/interpreter",
#        gdf=True
#        ):
#    """
#    Description
#    -----------
#    Get OSM data with key/value pair and that is Polygon by making
#    queries on Overpass
#    
#    Return
#    ------
#    GeoJSON Polygons FeatureCollection
#    
#    Parameters
#    ----------
#    - bbox(tuple):
#        - bounding box for the query
#        - must be (SOUTH, WEST, NORTH, EAST)
#        - must be EPSG 4326 (WGS84) projection
#        - ex: (45.772, 4.864, 45.778, 4.875)
#    - key(str):
#        - key for the OSM query
#    - value(str):
#        - value for the OSM query
#    - timeout(int):
#        - time in seconds for the timeout
#        - default: 40
#    - endpoint(str):
#        - endpoint for the queries
#        - default: "https://overpass-api.de/api/interpreter"
#    - gdf(boolean):
#        - if GeoDataFrame for output
#        - default: True
#    """
#    
#    #if bbox is list, transform to tuple
#    if isinstance(bbox, list):
#        bbox = tuple(bbox)
#    api = overpass.API(
#            timeout=timeout, 
#            endpoint=endpoint
#            )
#    if value == "all":
#        requ =  """
#        (
#            node["{0}"]{1};
#            way["{0}"]{1};
#            relation["{0}"]{1};
#        );
#        (._;>;);
#        out geom;
#        """.format(key,bbox)
#    else:
#        requ =  """
#        (
#            node["{0}"="{1}"]{2};
#            way["{0}"="{1}"]{2};
#            relation["{0}"="{1}"]{2};
#        );
#        (._;>;);
#        out geom;
#        """.format(key, value,bbox)
#        
#    data = api.get(requ, verbosity='geom', responseformat="geojson")
#    polys_geojson = _from_lines_to_polys(data, key, value)
#    
#    if gdf == True:
#        polys = gpd.GeoDataFrame.from_features(polys_geojson)
#        polys = polys.dropna(axis=1, how='all')
#        polys.crs = {"init":"epsg:4326"}
#        #Try to avoid wrong geometry by buffering with 0
#        polys["new_geom"] = polys["geometry"].buffer(0) 
#        polys = polys.rename(
#                columns={
#                        "geometry":"old_geometry"
#                        }
#                )
#        polys = polys.rename(
#                columns={
#                        "new_geom":"geometry"
#                        }
#                ).set_geometry("geometry")
#        polys.drop("old_geometry", inplace=True, axis=1)
#        
#        return polys
#    
#    else:
#        return polys_geojson

# Try to avoid using overpass that is not a conda package
# Try to use osmnx instead
# TODO: remove commented section above if not needed after changes

def get_OSM_poly(
        bbox, 
        key, 
        value="all"
        ):
    """
    Description
    -----------
    Get OSM data with key/value pair and that is Polygon by making
    queries on Overpass
    
    Return
    ------
    GeoDataFrame
    
    Parameters
    ----------
    - bbox(tuple):
        - bounding box for the query
        - must be (SOUTH, WEST, NORTH, EAST)
        - must be EPSG 4326 (WGS84) projection
        - ex: (45.772, 4.864, 45.778, 4.875)
    - key(str):
        - key for the OSM query
    - value(str):
        - value for the OSM query
    """
    
    #Get GDF using osmnx
    gdf = ox.footprints.create_footprints_gdf(
            north=bbox[2], 
            south=bbox[0], 
            west=bbox[1], 
            east=bbox[3], 
            footprint_type=key
            )
    
    #Filter if necessary
    if value != "all":
        gdf = gdf.loc[gdf[key] == value]
    
    #Remove columns containing lists (to avoid Fiona writing crashes)
    for col in gdf.columns:
        if isinstance(gdf[col].iloc[0], list):
            gdf.drop(col, axis=1, inplace=True)
    
    return gdf
    

def _add_feature(features, feature):
    """
    
    """
    if len(feature.geometry["coordinates"]) > 3:
        geometry = geojson.Polygon(
            [
                feature.geometry["coordinates"]
            ]
        )
        feature.properties.update({"osm_id":feature.id})
        new_feature = geojson.Feature(
            geometry = geometry,
            properties = feature.properties
        )
        features.append(new_feature)
            
    return features

def _from_lines_to_polys(data, key, value):
    """
    Description
    -----------
    Transform OSM data from LineStrings to Polygons
    
    Return
    ------
    GeoJSON Polygons FeatureCollection
    
    Parameters
    ----------
    - data(json):
        - json from OSM query
    - key(str):
        - key used for the OSM query
    - value(str):
        - value used for the OSM query
    """
    data = geojson.loads(json.dumps(data))
    features = []
    for feature in data.features:
        if (feature.geometry["type"] == "LineString"):
            if value == "all":
                features = _add_feature(features, feature)
            else:
                if (
                    key in feature.properties and feature.properties[key] == value
                ):
                    features = _add_feature(features, feature) 
            
    return geojson.FeatureCollection(features)