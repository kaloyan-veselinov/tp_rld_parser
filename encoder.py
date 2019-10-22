from geojson import Point, Feature, FeatureCollection


class DataPoint:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def get_geojson_point(self) -> Point:
        return Point((self.longitude, self.latitude))

    def get_pin_color(self) -> str:
        return "#FFF"

    def get_geojson_feature(self):
        return Feature(
            geometry=self.get_geojson_point(),
            properties={'marker-color': self.get_pin_color()}
        )


class RSSIDataPoint(DataPoint):
    def __init__(self, latitude: float, longitude: float, rssi: float):
        super(RSSIDataPoint, self).__init__(latitude=latitude, longitude=longitude)
        self.rssi = rssi

    def get_pin_color(self) -> str:
        return "#FF0000"


if __name__ == "__main__":
    d1 = RSSIDataPoint(latitude=45.7837, longitude=4.8724, rssi=-107)
    d2 = RSSIDataPoint(latitude=45.7859, longitude=4.8783, rssi=-113)
    feature_collection: FeatureCollection = FeatureCollection([d1.get_geojson_feature(), d2.get_geojson_feature()])
    print(feature_collection)

