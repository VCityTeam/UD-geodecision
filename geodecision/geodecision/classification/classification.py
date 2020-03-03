#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 12:29:09 2019

@author: thomas
"""

import json
import geopandas as gpd
import mapclassify as mc
import os
import time

from ..logger.logger import logger, _get_duration

#from constants_vars import gridded_data_var


class ClassificationDataFrames:
    """
    Description
    ------------
    
    Make automatic classifications for chosen pandas Series in a (Geo)DataFrame.
    Classification based on mapclassify 
    (https://pysal.org/mapclassify/index.html)
    
    Returns
    --------
    
    Dict:
        {"name": {DataFrame with classes 
        Dictionaries of classification (results, bests, bins interval)
    
    Parameters
    -----------
    
    - params(json file):
        - json with parameters:
            [{
                "name": "name of the futur GeoDataFrame A",
                "filepath": "path/to/GeoJSON file",
                "variables": {
                    "variable 1": {
                        "classification": boolean (if true, make classification, else set to false),
                        "description": "Short description of the var"
                    },
                    "variable 2": {
                        "classification": boolean (if true, make classification, else set to false),
                        "description": "Short description of the var"
                    },
                    "variable 3": {
                        "classification": boolean (if true, make classification, else set to false),
                        "description": "Short description of the var"
                    }
                },
                {
                    "name": "name of the futur GeoDataFrame A",
                    "filepath": "path/to/GeoJSON file",
                    "variables": {
                        "variable 1": {
                            "classification": boolean (if true, make classification, else set to false),
                            "description": "Short description of the var"
                        },
                        "variable 2": {
                            "classification": boolean (if true, make classification, else set to false),
                            "description": "Short description of the var"
                        },
                        "variable 3": {
                            "classification": boolean (if true, make classification, else set to false),
                            "description": "Short description of the var"
                        }
                    }
                }
            ]
    """
    def __init__(self, params):
        """
        Description
        ------------
        Initializes and runs all
        
        Returns
        --------
        
        Dictionary with (for each element in JSON parameters list)
            - Results of classification 
            - Best classigication  (name, classification, intervals)
            - GeoDataFrame 
            (input GeoDataFrame with classifications for each chosen field)
        
        """
        #TODO: improve and simplify all of this. Add long name of element
        with open(params) as f:
            params = json.load(f)
          
        self.dict_ = {}
        
        for element in params:
            vars_classification = {}
            gdf = gpd.GeoDataFrame.from_file(element["filepath"])
            output_dir = element["output_dir"]
            driver = element["driver"]
            if driver == "GPKG":
                extension = ".gpkg"
                layer = "classified"
            elif driver == "GeoJSON":
                extension = ".geojson"
            else:
                raise ValueError("No driver, written with default: GPKG")
                extension = ".gpkg"
                layer = "classified"
            
            for variable in element["variables"]:
                if element["variables"][variable]["classification"] is True:
                    start = time.time()
                    vars_classification[
                            variable
                            ] = self._get_best_classification(
                    gdf[variable]
                    )
                    
                    logger.info(
                            "Element {}, variable {}, duration => {}".format(
                                    element["name"],
                                    variable,
                                    _get_duration(start)
                                    )
                            )
                    
                    print(
                            "Element {}, variable {}, duration => {}".format(
                                    element["name"],
                                    variable,
                                    _get_duration(start)
                                    )
                            )

            if element["name"] in self.dict_:
                self.dict_[element["name"]].update(vars_classification) 
            else:
                self.dict_[element["name"]] = vars_classification 
                
            self.dict_[element["name"]]["gdf"] = self._attribute_class(
                    gdf,
                    element["name"] 
                    )
            
            filepath = os.path.join(
                    output_dir,
                    element["name"] + "_classified" + extension
                    )
            
            if layer: 
                self.dict_[element["name"]]["gdf"].to_file(
                        filepath, 
                        layer=layer,
                        driver=driver
                        )
            else:
                self.dict_[element["name"]]["gdf"].to_file(
                        filepath, 
                        driver=driver
                        )
    
    def _get_interval(self, bins):
        """
        Description
        ------------
        
        Get intervals (low, high and name of the interval) from bins
        
        Returns
        --------
        
        List of dicts(low, high, name)
        
        Parameters
        -----------
        
        - bins(mapclassify.classifiers classification)
        see: https://pysal.org/mapclassify/generated/mapclassify.KClassifiers.html

        """
        intervals = []
        intervals.append(
                {
                        "low": 0, 
                        "high": bins[0],
                        "name": "0" + " <= " + str(bins[0])
                        }
                )
        for i,bin_ in enumerate(bins[:-1]):
            intervals.append(
                    {
                            "low": bin_, 
                            "high": bins[i+1],
                            "name": str(bin_) + " <= " + str(bins[i+1])
                            }
                    )
        
        return intervals
        
    def _get_best_classification(self, serie):
        """
        Description
        ------------ 
        
        Get the best classification for a GeoPandas Serie
        
        Returns
        --------
        
        Dictionary:
            - "results": detailed results of the mapclassify classification 
            - "best":
                - "all": results of best classification 
                - "name": best classification name 
                - "intervals": intervals from bins 
        
        Parameters
        -----------
        
        - serie(GeoPandas Serie)
        

        """
        ks = mc.classifiers.KClassifiers(serie)
        return {
                "results": ks.results,
                "best": {
                        "all" : ks.best,
                        "name" : ks.best.name,
                        "intervals" : self._get_interval(ks.best.bins)
                        }
                }
        
    def _attribute_class(self, gdf, name):
        """
        Description
        ------------ 
        
        Apply classification on GeoDataFrame to get classes for futur uses
        Inspired by: https://stackoverflow.com/a/36423625
        
        Returns
        --------
        
        GeoDataFrame with classifications
        
        
        Parameters
        -----------
        - gdf (GeoDataFrame)
        - name (str): name of GeoDataFrame in self.dict_
        

        """
        
        for col in gdf:
            if col in self.dict_[name]:
                df = gpd.pd.DataFrame(
                        self.dict_[name][col]["best"]["intervals"]
                        )
                bins = list(df["high"])
                bins.insert(0,0)
                new_col = col + "(" + self.dict_[name][col]["best"]["name"] + ")"
                gdf[new_col] = gpd.pd.cut(
                        gdf[col], 
                        bins, 
                        labels = df["name"]
                        )
                #Need to convert categorical serie to string in order to write them
                gdf[new_col] = gdf[new_col].astype("str")
        return gdf
            