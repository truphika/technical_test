from typing import NamedTuple

from geopandas import GeoDataFrame
from pandas import Series
from shapely import Point


class ProximityData(NamedTuple):
    nearby_points: GeoDataFrame
    distances_to_point: Series
    point: Point
