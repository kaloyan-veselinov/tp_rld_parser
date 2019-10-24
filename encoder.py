import errno
import os
from typing import List, Dict

import geojson
from geojson import Point, Feature, FeatureCollection

from processor import Gateway, AveragedMesure


class DataPoint:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def get_geojson_point(self) -> Point:
        return Point((self.longitude, self.latitude))

    def get_pin_color(self) -> str:
        return "#FFF"

    def get_geojson_feature(self) -> Feature:
        return Feature(
            geometry=self.get_geojson_point(),
            properties={'marker-color': self.get_pin_color()}
        )

    @staticmethod
    def get_geojson_feature_collection(data_points: List['DataPoint']) -> FeatureCollection:
        return FeatureCollection([d.get_geojson_feature() for d in data_points])

    @staticmethod
    def export(collection: FeatureCollection, filename: str):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filename, "w") as f:
            geojson.dump(collection, f)


class RSSIDataPoint(DataPoint):
    def __init__(self, latitude: float, longitude: float, rssi: float):
        super(RSSIDataPoint, self).__init__(latitude=latitude, longitude=longitude)
        self.rssi = rssi

    def get_geojson_feature(self) -> Feature:
        return Feature(
            geometry=self.get_geojson_point(),
            properties={
                'RSSI (dBm)': str(self.rssi),
                'marker-color': self.get_pin_color()
            }
        )

    def get_pin_color(self) -> str:
        if self.rssi > -65:
            return "#008000"
        if self.rssi > -70:
            return "#00FF00"
        if self.rssi > -75:
            return "#00FFFF"
        if self.rssi > -80:
            return "#FFFF00"
        if self.rssi > -85:
            return "#FFA500"
        if self.rssi > -90:
            return "#FF00FF"
        if self.rssi > -95:
            return "#800080"
        if self.rssi > -100:
            return "#0000FF"
        if self.rssi > -105:
            return "#000080"
        if self.rssi > -110:
            return "#FF0000"
        if self.rssi > -115:
            return "#800000"
        if self.rssi > -120:
            return "#000000"

        return "#FFF"


class GatewayDataPoint(DataPoint):
    def __init__(self, latitude: float, longitude: float, id: str):
        super(GatewayDataPoint, self).__init__(latitude=latitude, longitude=longitude)
        self.id = id

    def get_pin_color(self) -> str:
        return "#808080"

    def get_geojson_feature(self) -> Feature:
        return Feature(
            geometry=self.get_geojson_point(),
            properties={
                'Gateway ID': str(self.id),
                'marker-color': self.get_pin_color()
            }
        )


class ClusterDataPoint(DataPoint):
    def __init__(self, latitude: float, longitude: float, cluster_id: int):
        super(ClusterDataPoint, self).__init__(latitude=latitude, longitude=longitude)
        self.cluster_id = cluster_id

    def get_pin_color(self) -> str:
        colors = ["#800000", "#FF0000", "#FFA500", "#FFFF00", "#808000", "#008000", "#800080", "#FF00FF", "#00FF00",
                  "#008080", "#00FFFF", "#0000FF", "#000080", "#000000", "#808080", "#C0C0C0", "#FFFFFF"]
        return colors[(self.cluster_id + 1) % len(colors)]

    def get_geojson_feature(self) -> Feature:
        return Feature(
            geometry=self.get_geojson_point(),
            properties={
                'Cluster id': str(self.cluster_id),
                'marker-color': self.get_pin_color()
            }
        )


def create_gateways_map(gateways: Dict[str, Gateway]) -> FeatureCollection:
    gateway_data_points: List[GatewayDataPoint] = [GatewayDataPoint(
        latitude=g.latitude,
        longitude=g.longitude,
        id=g.gw_id
    ) for g in gateways.values()]
    return DataPoint.get_geojson_feature_collection(gateway_data_points)


def create_gateways_rssi_coverage_maps(gateways: Dict[str, Gateway],
                                       gateways_coverage: Dict[str, List[AveragedMesure]]) -> Dict[
    str, FeatureCollection]:
    rssi_coverage_maps: Dict[str, FeatureCollection] = {}
    for gw_id, avg_mesures in gateways_coverage.items():
        if gw_id in gateways:
            data_points: List[DataPoint] = [RSSIDataPoint(
                latitude=m.latitude,
                longitude=m.longitude,
                rssi=m.max_gateway_rssi) for m in avg_mesures]
            gw = gateways[gw_id]
            data_points.insert(0, GatewayDataPoint(
                latitude=gw.latitude,
                longitude=gw.longitude,
                id=gw.gw_id
            ))
            rssi_coverage_maps[gw_id] = DataPoint.get_geojson_feature_collection(data_points)

    return rssi_coverage_maps


def create_rssi_coverage_map_by_sf(coverage_by_sf: Dict[str, List[AveragedMesure]]) -> Dict[str, FeatureCollection]:
    rssi_coverage_map_by_sf: Dict[str, FeatureCollection] = {}
    for sf, avg_mesures in coverage_by_sf.items():
        data_points: List[DataPoint] = [RSSIDataPoint(
            latitude=m.latitude,
            longitude=m.longitude,
            rssi=m.max_gateway_rssi) for m in avg_mesures]

        rssi_coverage_map_by_sf[sf] = DataPoint.get_geojson_feature_collection(data_points)

    return rssi_coverage_map_by_sf


def create_cluster_map(clusters: Dict[int, List['Mesure']]) -> FeatureCollection:
    cluster_data_points: List[ClusterDataPoint] = []
    for cluster_id, mesures in clusters.items():
        for m in mesures:
            cluster_data_points.append(ClusterDataPoint(
                latitude=m.latitude,
                longitude=m.longitude,
                cluster_id=cluster_id
            ))

    return DataPoint.get_geojson_feature_collection(cluster_data_points)
