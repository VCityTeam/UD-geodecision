#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 18:12:36 2020

@author: thomas
"""
                    
def set_para(gdf, selection, sliders):
    str_ = """
             <!DOCTYPE html>
            <html>
            <head>
            <style>
            table {
              border-collapse: collapse;
              width: 100%;
            }
            
            th, td {
              text-align: left;
              padding: 6px;
              font-size:10px
            }
            
            tr:nth-child(even) {background-color: #7ec8ffff;}
            </style>
            </head>
            <body>
            
            <h4>Synthetic results</h4>
            
            <table>
            """
    nb_roofs = len(gdf)
    for k,v in sliders.items():
        str_ += """
                <tr>
                  <th>% of roofs with {} in range [ {} <= x < {} ]</th>
                  <th><b>{} %</b></th>
                </tr>
                """.format(
                k,
                v.value[0],
                v.value[1],
                round(
                        len(
                                gdf.loc[
                                        (gdf[k] >= v.value[0]) 
                                        & (gdf[k] < v.value[1])
                                        ]
                                ) / nb_roofs * 100
                        )
                )
    
    str_ += """
             <tr>
                  <th>Number of roofs with potential</th>
                  <td><b>{}</b></td>
             </tr>
            """.format(
            len(selection)
            )
    str_ += """
             <tr>
                  <th>Total number of roofs of the layer </th>
                  <td><b>{}</b></td>
             </tr>
            """.format(
            nb_roofs
            )
    str_ += """
             <tr>
                  <th>% of roofs with potential </th>
                  <td><b>{}%</b></td>
             </tr>
            """.format(
            round(len(selection) / nb_roofs * 100) 
            )
    str_ += """
             <tr>
                  <th>Total roofs area (m²)</th>
                  <td><b>{}</b></td>
             </tr>
            """.format(
            round(gdf.area.sum())  
            )
    str_ += """
             <tr>
                  <th>Roofs area with potential (m²)</th>
                  <td><b>{}</b></td>
             </tr>
            """.format(
            round(selection.area.sum()) 
            )
    str_ += """
             <tr>
                  <th>% of potential roofs area</th>
                  <td><b>{}%</b></td>
             </tr>
            """.format(
            round(selection.area.sum()/gdf.area.sum() * 100) 
            )
    str_ += """
            </table>
            </body>
            """
    return str_