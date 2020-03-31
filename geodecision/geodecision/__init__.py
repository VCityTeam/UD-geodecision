"""Top-level package for geodecision."""

__author__ = """Thomas Leysens"""
__email__ = 'thomleysens@gmail.com'
__version__ = '0.1.0'

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .accessibility.accessibility import run
from .accessibility.isochrone import Accessibility
from .classification.classification import ClassificationDataFrames
from .graph.connectpoints import ConnectPoints
from .graph.splittednodes import GetSplitNodes
from .graph.utils import graph_to_df, df_to_graph
from .osmquery.methods import get_OSM_poly
from .spatialops.operations import SpatialOperations, gdf_to_geosource
from .spatialops.intersections import GetIntersections
from .citygml.analyseroofs import GetRoofsAndSlopes
