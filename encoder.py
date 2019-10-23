from typing import List, Dict

from geojson import Point, Feature, FeatureCollection

from processor import Gateway


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


class RSSIDataPoint(DataPoint):
    def __init__(self, latitude: float, longitude: float, rssi: float):
        super(RSSIDataPoint, self).__init__(latitude=latitude, longitude=longitude)
        self.rssi = rssi

    def get_pin_color(self) -> str:
        return "#FF0000"


class GatewayDataPoint(DataPoint):
    def __init__(self, latitude: float, longitude: float, id: str):
        super(GatewayDataPoint, self).__init__(latitude=latitude, longitude=longitude)
        self.id = id

    def get_pin_color(self) -> str:
        return "#FF0000"

    def get_geojson_feature(self) -> Feature:
        return Feature(
            geometry=self.get_geojson_point(),
            properties={
                'name': self.id,
                'marker-color': self.get_pin_color()
            }
        )


def create_gateways_map(gateways: Dict[str, Gateway]):
    gateway_data_points: List[GatewayDataPoint] = [GatewayDataPoint(
        latitude=g.latitude,
        longitude=g.longitude,
        id=g.gw_id
    ) for g in gateways.values()]
    return DataPoint.get_geojson_feature_collection(gateway_data_points)


if __name__ == "__main__":
    d1 = RSSIDataPoint(latitude=45.7837, longitude=4.8724, rssi=-107)
    d2 = RSSIDataPoint(latitude=45.7859, longitude=4.8783, rssi=-113)
    feature_collection: FeatureCollection = DataPoint.get_geojson_feature_collection([d1, d2])
    print(feature_collection)

