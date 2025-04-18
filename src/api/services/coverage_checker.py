import geopandas
from shapely import Point
from api.entities.network_coverage import NetworkCoverage
from api.entities.point import DecimalDegreePoint
from pyproj import Transformer
from api.logger import logger
from api.entities.proximity_data import ProximityData


class CoverageChecker:
    TECH_COVERAGE = {"2G": 30000, "3G": 5000, "4G": 10000}

    def __init__(self, dataset: list[dict]) -> None:
        self.dataset = dataset
        for data in dataset:
            data["geometry"] = Point(data["x"], data["y"])
        geo_dataframe = geopandas.GeoDataFrame(
            dataset, geometry="geometry", crs="EPSG:2154"
        )

        self.geo_dataframe = geo_dataframe
        self.spatial_index = self.geo_dataframe.sindex
        self.operators = geo_dataframe["Operateur"].unique()
        logger.debug(
            f"CoverageChecker created with {self.geo_dataframe['geometry'].size} mobile sites"
        )
        logger.debug(f"CoverageChecker created with operators: {self.operators}")

    def _is_covered_by_tech(
        self,
        proximity_data: ProximityData,
        network_operator: str,
        network_tech: str,
    ) -> bool:
        point_within_tech_radius = proximity_data.nearby_points[
            proximity_data.distances_to_point <= self.TECH_COVERAGE[network_tech]
        ]
        point_covered_by_operator = point_within_tech_radius[
            point_within_tech_radius[network_tech] == 1
        ]
        is_tech_covered = any(
            point_covered_by_operator["Operateur"] == network_operator
        )

        logger.trace(
            f"Point {proximity_data.point}, found {point_covered_by_operator['geometry'].size} mobile site "
            f"in {network_tech} coverage radius for operator {network_operator}"
        )
        logger.trace(
            f"Point {proximity_data.point}, {'covered' if is_tech_covered else 'not covered'} "
            f"for {network_tech} by operator {network_operator}"
        )

        return is_tech_covered

    def _get_operator_coverage(
        self,
        proximity_data: ProximityData,
        network_operator: str,
    ) -> NetworkCoverage:
        coverage = NetworkCoverage(
            supports_2G=self._is_covered_by_tech(
                proximity_data, network_operator, "2G"
            ),
            supports_3G=self._is_covered_by_tech(
                proximity_data, network_operator, "3G"
            ),
            supports_4G=self._is_covered_by_tech(
                proximity_data, network_operator, "4G"
            ),
            operator=network_operator,
        )

        logger.debug(f"Point: {proximity_data.point}, coverage: {coverage}")

        return coverage

    def _get_proximity_data(self, point: Point) -> ProximityData:
        buffer = point.buffer(self.TECH_COVERAGE["2G"])
        possible_matches_index = list(self.spatial_index.intersection(buffer.bounds))
        possible_matches = self.geo_dataframe[
            self.geo_dataframe.index.isin(possible_matches_index)
        ]
        distances = possible_matches.geometry.distance(point)
        logger.debug(
            f"Point {point}, found {possible_matches['geometry'].size} mobile site in 2G coverage radius"
        )

        return ProximityData(possible_matches, distances, point)

    def _get_all_operator_coverage(self, point: Point) -> list[NetworkCoverage]:
        proximity_data = self._get_proximity_data(point)
        operators_result = [
            self._get_operator_coverage(proximity_data, network_operator)
            for network_operator in self.operators
        ]

        return operators_result

    def get_point_coverage(self, point: DecimalDegreePoint) -> list[NetworkCoverage]:
        crs_transformer = Transformer.from_crs(4326, 2154, always_xy=True)
        inp = Point(point.long, point.lat)
        p = Point(crs_transformer.transform(inp.x, inp.y))

        logger.debug(f"Point: {point}, projected to ESPG:2154: {p}")

        coverage = self._get_all_operator_coverage(p)

        return coverage
