from typing import List

from geojson import Point, Feature, FeatureCollection


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


if __name__ == "__main__":
    d1 = RSSIDataPoint(latitude=45.7837, longitude=4.8724, rssi=-107)
    d2 = RSSIDataPoint(latitude=45.7859, longitude=4.8783, rssi=-113)
    feature_collection: FeatureCollection = DataPoint.get_geojson_feature_collection([d1, d2])
    print(feature_collection)

