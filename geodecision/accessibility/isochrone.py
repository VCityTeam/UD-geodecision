#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:43:42 2019

@author: thomas
"""
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point, LineString
from shapely import speedups
from collections import namedtuple
from bokeh.palettes import Viridis, Viridis256
import time
import pandas as pd

from ..spatialops.operations import get_intersect_matches
from ..logger.logger import _get_duration, logger

speedups.enable()

GeoData = namedtuple("GeoData", ["origin","metric","vis"])
EPSG = namedtuple("EPSG", ["origin", "metric", "vis"])

class Accessibility:
    """
    Description:
    ------------ 
    
    Measure accessibility on a graph (with time as weight on edges) from a 
    list of points and a list of durations. 
    
    Inspired by:
        https://github.com/gboeing/osmnx-examples/blob/master/notebooks/13-isolines-isochrones.ipynb
        http://kuanbutts.com/2017/12/16/osmnx-isochrones/
    
    Returns:
    --------
    Add to the class object:
        - Isolines:
            - object.lines.origin => isolines with origin EPSG
            - object.lines.metric => isolines with metric EPSG
            - object.lines.vis => isolines with visualisation EPSG
        - Buffered isolines:
            - object.buffered.origin => buffered isolines with origin EPSG
            - object.buffered.metric => buffered isolines with metric EPSG
            - object.buffered.vis => buffered isolines with visualisation EPSG
        - Union of buffered isolines by duration:
            - object.union.origin => union of buffered isolines with origin EPSG
            - object.union.metric => union of buffered isolines with metric EPSG
            - object.union.vis => union of buffered isolines with visualisation EPSG
  
    Parameters:
    -----------
    - G(NetworkX graph):
        - Graph with time weighted edges
        - MultiDiGraph
    - trip_times(list):
        - list of integer values
        - durations value for making isochrones 
    - distance_buffer(int):
        - value in meters for buffering isolines
    - weight(str):
        - name of the weight/duration field used to measure accessibility
    - center_nodes(list):
        - list of nodes from which to measure accessibility
    - input_polygons(Shapely Polygons):
        - Input polygons from which center_nodes have been deducted
    - palette(dict):
        - dict of colors:
            => {1:"#hexcolor1", 2:"hexcolor2"}
        - default: Viridis Bokeh palette
    - epsg(dict):
        - dict of EPSG values (origin, metric, visualisation)
        - => metric EPSG is needed to measure buffers in meters, origin EPSG 
        is needed to set the default and visualisation is needed to get 
        elements set for webmapping (example: EPSG 3857)
        - default:
            => epsgs={
                    "origin":"4326",
                    "metric":"2154",
                    "vis":"3857"
                    }
    """
    
    #TODO: complete the documentation of the class
    
    def __init__(
        self, 
        G, 
        trip_times, 
        distance_buffer,
        weight,
        center_nodes,
        input_polygons,
        palette=Viridis,
        epsgs={
                "origin":"4326",
                "metric":"2154",
                "vis":"3857"
                }
        ):
        """
        Description:
        ------------
        
        Init: see Class
        """
        #TODO: delete this if not anymore required (need to think about it)
#        if center_nodes == [] and pts != []:
#            xs, ys = map(list, zip(*pts))
#            self.center_nodes = ox.get_nearest_nodes(
#                    G,
#                    xs, 
#                    ys, 
#                    method="kdtree"
#                    )
#        else:
#            self.center_nodes = center_nodes
        
        self.center_nodes = center_nodes
        
        #Handle case when only one value in trip_times 
        # to avoid error getting palette (min. 3) 
        colors_times = [0]
        colors_times.extend(trip_times)
        if len(colors_times) > 11:
            palette = Viridis256
            self.colors = {
            trip_time:color for trip_time,color in zip(
                        colors_times, 
                        palette[colors_times[0]:colors_times[-1]+1]
                        )
                }
        elif (len(colors_times) <=11) and  (len(colors_times) > 2):
            self.colors = {
                trip_time:color for trip_time,color in zip(
                        colors_times, 
                        palette[len(colors_times)]
                        )
                }
        elif len(colors_times) == 2:
            self.colors = {
                    colors_times[0]:palette[3][0],
                    colors_times[1]:palette[3][1]
                    }
        else:
            self.colors = {
                    colors_times[0]:palette[3][0]
                    }
            
        self.G = G
        self.trip_times = trip_times
        self.distance_buffer = distance_buffer
        self.input_polygons = input_polygons
        self.epsgs = EPSG(
                epsgs["origin"],
                epsgs["metric"],
                epsgs["vis"]
                )
        self.weight = weight
        self.iso_cat = "iso_cat"
        self.iso_cat_merged = self.iso_cat + "_merged"
        
    
    def get_subgraph(self, center_node, trip_time):
        """
        Description:
        ------------
        
        Get a NetworkX subgraph regarding the trip_time and get nodes and 
        edges to make Shapely LineString
        
        Parameters:
        -----------
        - center_node(NetworkX node):
            - node from which ego_graph is measured
        - trip_time(int): 
            - radius in time for the ego_graph
            
        """
        if self.G.has_node(center_node):
            subgraph = nx.ego_graph(
                    self.G, 
                    center_node, 
                    radius=trip_time, 
                    distance= self.weight
                    )
            node_points = [
                    Point(
                            (
                                    data['x'],
                                    data['y']
                                    )
                            ) for node, data in subgraph.nodes(data=True)
                    ]
            
            if len(node_points) > 1: 
                nodes_gdf = gpd.GeoDataFrame(
                        {
                                'id': subgraph.nodes()
                                }, 
                        geometry=node_points
                        )
                self.nodes_gdf = nodes_gdf.set_index('id')
                df_edges = nx.to_pandas_edgelist(subgraph)
                df_edges["from"] = df_edges["source"].map(
                        self._get_geom_df
                        )
                df_edges["to"] = df_edges["target"].map(
                        self._get_geom_df
                        )  
                df_edges["line"] = df_edges.apply(
                        lambda x: LineString([x["from"], x["to"]]),
                        axis=1
                        )
                #Name the new duration field with self.weight 
                ##and trip_time value
                duration_name = self.iso_cat + "_" + str(trip_time)
                df_edges[duration_name] = trip_time
                df_edges["color"] = self.colors[trip_time]
            
            self.l_gdf.append(df_edges)
        else:
            self.pb_nodes.append(center_node)
    
    def _make_iso_lines(self):
        """
        Description:
        ------------
        Get isolines and returns a GeoDataFrame
            
        """
        
        self.l_gdf = []
        self.pb_nodes = []

        for trip_time in self.trip_times:
            for center_node in self.center_nodes:
                self.get_subgraph(center_node, trip_time)
        gdf = gpd.pd.concat(self.l_gdf, sort=False)
        
        #Get the min values for "iso_cat" and update gdf with these min values
        columns_ = [
                self.iso_cat + "_" + str(trip_time) for trip_time in self.trip_times
                ]
        #Make a new dataframe with no source/target couple duplicates
        self.gdf = gdf[
                [col for col in gdf.columns if col not in columns_]
                ].drop_duplicates(["source", "target"])
        gdf[self.iso_cat] = gdf[columns_].min(axis=1)
        ## groupby source/target and get the "iso_cat" minimum value
        ### first need to make a unique id for source/target target/source
        ### because we don't, for now, want an A=>B edge covered by a B=>A edge
#        gdf["source_target"] = gdf["source"] + gdf["target"] 
        tmp = gdf.groupby(["source", "target"])["iso_cat"].min()
        ## and merge with gdf 
        self.gdf = pd.merge(
                self.gdf, 
                tmp, 
                how="left", 
                on=["source", "target"]
                )
        
        # Use frozenset to find the min value of source/target, 
        ##target/source couples
        self.gdf["frozenset"] = self.gdf.apply(
                lambda x: frozenset((x["source"],x["target"])),
                axis=1
                )
        mins = self.gdf.groupby(["frozenset"])[self.iso_cat].min()
        self.gdf = pd.merge(
                self.gdf, 
                mins, 
                how="left", 
                on="frozenset",
                suffixes=("_base", "_merged")
                ).drop_duplicates(
                        ["frozenset", self.iso_cat_merged]
                        )
        dict_ = self.gdf[
                ["source", "target", self.iso_cat_merged]
                ].to_dict(orient="list")
        updates = []
        for source,target,value in zip(
                dict_["source"],
                dict_["target"],
                dict_[self.iso_cat_merged]
                ):
            updates.append(
                    (source, target, {"duration_name":value}) #TODO: fix the problem of the name
                    )
        self.G.update(edges=updates)
    
    def get_results(self):
        """
        Description:
        ------------
        
        Get isolines GeoDataFrame
        Make buffered isolines (polygons)
        Make union of buffered isolines by duration
        Add these elements to the class
        
        """        
        start = time.time()
        self._make_iso_lines()
        logger.info(
                """
                | Isochrone.py |
                | Accessibility.get_results |
                
                Making isolines:
                    Number of nodes: {}
                    Durations values: {}
                    Total time : {}
                """.format(
                    len(self.center_nodes),
                    self.trip_times,
                    _get_duration(start)
                )
                )
        gdf_lines = self.gdf[
                [
                 "source", 
                 "target", 
                 "from", 
                 "to", 
                 "line", 
                 self.weight, 
                 self.iso_cat_merged, 
                 "color"
                 ]
                ]
        gdf_lines = gdf_lines.drop_duplicates(
                subset=["source","target"]
                )
        gdf_lines = gdf_lines.rename(
                        columns={'line': 'geometry'}
                        ).set_geometry('geometry')
        gdf_lines.crs = {
                'init': "epsg:{}".format(
                        self.epsgs.origin
                        )
                }
        gdf_lines.to_crs(
                {
                        'init': "epsg:{}".format(
                                self.epsgs.metric
                                )
                        }, 
                inplace=True
                )
                
        # Reset index
        gdf_lines.reset_index(drop=True, inplace=True)
        # Attribute a specific category value to lines inside input polygons
        neutral_lines = get_intersect_matches(
                self.input_polygons, 
                gdf_lines
                )
        gdf_lines.iso_cat_merged.iloc[neutral_lines] = 0.0
        gdf_lines.color.iloc[neutral_lines] = self.colors[0]
        
        gdf_lines.drop(
                ['from','to'], 
                axis=1, 
                inplace=True
                )
        
        start = time.time()
        
        gdf_buffered_lines = gdf_lines[
                ["source", "target","geometry", "color", self.iso_cat_merged]
                ]
        gdf_buffered_lines["polys"] = gdf_buffered_lines.apply(
                        lambda x: x["geometry"].buffer(self.distance_buffer),
                        axis=1
                        )
        gdf_buffered_lines.drop(
                ['geometry'], 
                axis=1, 
                inplace=True
                )
        gdf_buffered_lines = gdf_buffered_lines.rename(
                columns={'polys': 'geometry'}
                ).set_geometry('geometry')
        logger.info(
                """
                | Isochrone.py |
                | Accessibility.get_results |
                
                Get buffered isolines:
                    Total time : {}
                """.format(
                    _get_duration(start)
                )
                )
        gdf_union = []
        for trip_time in self.trip_times:
            start = time.time()
            #TODO: add simplification if speed needed
            polys = gdf_buffered_lines.loc[
                    gdf_buffered_lines[self.iso_cat_merged]==trip_time
                    ]["geometry"].unary_union 
            gdf_buffered_lines_union = gpd.GeoDataFrame(geometry=[polys])
            gdf_buffered_lines_union[self.iso_cat_merged] = trip_time
            gdf_buffered_lines_union["color"] = self.colors[trip_time]
            gdf_buffered_lines_union.crs = {
                    'init': "epsg:{}".format(
                            self.epsgs.metric
                            )
                    }
            gdf_union.append(gdf_buffered_lines_union)
            logger.info(
                """
                | Isochrone.py |
                | Accessibility.get_results |
                
                Unary union for {} minutes layer:
                    Total time : {}
                """.format(
                    trip_time,
                    _get_duration(start)
                )
                )
        gdf_union = gpd.pd.concat(gdf_union, sort=False)
        self.lines = gdf_lines
        self.union = gdf_union
        self.buffered = gdf_buffered_lines
        
    def _change_crs(self, gdf, crs):
        """
        Description:
        ------------
        
        Change the CRS/EPSG of a GeoDataFrame
        
        Parameters:
        -----------
        
        - gdf(GeodDataFrame): 
            - GeoPandas GeoDataFrame 
        - crs(str):
            - CRS/EPSG output
        
        """
        
        gdf.to_crs(
                {
                        'init': "epsg:{}".format(crs)
                        }, 
                inplace=True
                )
        
        return gdf
    
    def _get_geom_df(self, node):
        """
        Description:
        ------------
        
        Get geometry of a node source or target
        Used to make LineStrings
        
        Parameters:
        -----------
        
        node(str): 
            - source or target graph node
        """
        
        return self.nodes_gdf.at[(
                node, 
                "geometry"
                )]