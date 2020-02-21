#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@author: thomleysens
"""
Created on Thu Feb 13 15:14:20 2020

@author: thomas
"""

import argparse
import os
import sys
import json
import geopandas as gpd

text = """
Get analysed roofs files
"""

#geodecision_path = os.path.abspath("../geodecision/")
#
#if geodecision_path not in sys.path:
#    sys.path.insert(0, geodecision_path)
    
from geodecision import GetRoofsAndSlopes


def run(json_config):
    """
    """
    #Load params JSON file
    with open(json_config) as f: 
        params = json.load(f)

    #Inputs
    epsg_in = params["epsg"]["in"]
    epsg_out = params["epsg"]["out"]
    gml_dir = params["dir"]["input"]
    output_dir = params["dir"]["output"]
    palette = params["settings"]["palette"]
    driver  = params["settings"]["driver"]
    attributes = params["settings"]["attributes"]
    tuples = []
    dfs = []
    gdfs = []
    dfs_buildings = []
    
    #Get a list of tuples input filenames, output filenames
    for gml_file in os.listdir(gml_dir):
        if gml_file.endswith(".gml"):
            name = os.path.splitext(gml_file)[0]
            name_gml = os.path.join(gml_dir, name + ".gml")
            tuples.append((name_gml, name, output_dir))
            
    #Get flat roofs
    for tuple_ in tuples:
        roofs = GetRoofsAndSlopes(
            tuple_[0], 
            epsg_in, 
            epsg_out,
            tuple_[1], 
            attributes = attributes,
            driver = driver, 
            out_dir = tuple_[2] 
        )
        dfs.append(roofs.df_roofs)
        gdfs.append(roofs.gdf_roofs)
        dfs_buildings.append(roofs.df_buildings)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description = text)
    parser.add_argument("json_config")
    args = parser.parse_args()
    run(args.json_config)