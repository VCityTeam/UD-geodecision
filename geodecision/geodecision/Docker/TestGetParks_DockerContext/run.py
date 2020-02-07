#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: thomas

import argparse
import os

from methods import get_OSM_poly, json

text = """
Get key/value spatial objects from OSM
"""


def run(json_config):
    """
    Run the methods with the parameters in JSON config file
    """
    #Load params JSON file
    with open(json_config) as f: 
        params = json.load(f)
    
    bbox = params["bbox"]
    key = params["key"]
    value = params["value"]
    driver = params["driver"]
    output_file = params["output_file"]
    features = get_OSM_poly(bbox, key, value)
    
    #Check if file exists, delete it if so before writting it 
    #(necessary because of Fiona behavior with GeoJSON)
    
    try:
        os.remove(output_file)
    except OSError:
        pass
    
    if driver == "GPKG":
        features.to_file(output_file, layer=key+"_"+value, driver=driver)
    else:
        features.to_file(output_file, driver=driver)
    
    print ("DONE")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description = text)
    parser.add_argument("json_config")
    args = parser.parse_args()
    run(args.json_config)