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

#To set middle height:
# Décret n°2002-120 du 30 janvier 2002 relatif aux caractéristiques du logement 
# décent pris pour l'application de l'article 187 de la loi n° 2000-1208 du 13 
# décembre 2000 relative à la solidarité et au renouvellement urbains. 
# Article 4

# + https://www.lemoniteur.fr/article/les-sept-principes-a-s-approprier.1953879
# WARNING: we don't have possibility to distinguish commercial/office buildings from 
# apartment blocks, yet they have not the same average height for level
AVG_HEIGHT = 2.70

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