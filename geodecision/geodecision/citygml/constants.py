#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
constants.py
@author: Thomas Leysens
"""

import numpy as np
from collections import namedtuple

REF_VECTOR = np.array([0,0,1])

NAMESPACES = {
    'ns0': "http://www.opengis.net/citygml/2.0",
    'ns1': "http://www.opengis.net/gml",
    'ns2': "http://www.opengis.net/citygml/building/2.0"
}

Coords = namedtuple("Coords", ["x","y","z"])
L_coords = namedtuple("L_coords", ["xs","ys", "zs"])

PUBLIC = ["église",
          "école",
          "université",
          "mairie",
          "stade",
          "cimetière",
          "gymnase",
          "salle",
          "lycée",
          "police",
          "clinique",
          "collège",
          "hôpital",
          "hospitalier",
          "médical"
          ]