import json
import sys
from json.decoder import JSONObject
from typing import List

from encoder import RSSIDataPoint

from processor import get_clusters, AveragedMesure, filter_mesures_by_sf


class Gateway:
    def __init__(self, id: str, rssi: int, snr: float, latitude: float, longitude: float):
        self.id = id
        self.rssi = rssi
        self.snr = snr
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'id: {self.id} rssi: {self.rssi} snr: {self.snr} latitude: {self.latitude} longitude: {self.longitude}'


class Mesure:
    def __init__(self, device_id: str, counter: int, data_rate: str, coding_rate: str, latitude: float,
                 longitude: float,
                 temperature: int, humidity: int, gateways: List[Gateway]):
        self.device_id = device_id
        self.counter = counter
        self.data_rate = data_rate
        self.coding_rate = coding_rate
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.humidity = humidity
        self.gateways = gateways

    # def __repr__(self):
    #     return self.__str__()

    def __str__(self):
        return f'data_rate: {self.data_rate} latitude: {self.latitude} longitude: {self.longitude} temperature: {self.temperature} humidity: {self.humidity} gateways: {self.gateways}'

    def __eq__(self, other):
        return self.device_id == other.device_id and self.counter == other.counter

    def __ne__(self, other):
        return not self.__eq__(other)



def parse_gateway_from_json(gateway_data: JSONObject) -> Gateway:
    return Gateway(
        id=gateway_data['gtw_id'],
        latitude=gateway_data['latitude'] if 'latitude' in gateway_data else None,
        longitude=gateway_data['longitude'] if 'longitude' in gateway_data else None,
        rssi=gateway_data['rssi'],
        snr=gateway_data['snr']
    )


def parse_mesure_from_json(mesure_data: JSONObject) -> Mesure:
    return Mesure(
        device_id=mesure_data['dev_id'],
        counter=mesure_data['counter'],
        data_rate=mesure_data['metadata']['data_rate'],
        coding_rate=mesure_data['metadata']['coding_rate'],
        latitude=mesure_data['payload_fields']['latitude'],
        longitude=mesure_data['payload_fields']['longitude'],
        temperature=mesure_data['payload_fields']['temperature'],
        humidity=mesure_data['payload_fields']['humidity'],
        gateways=[parse_gateway_from_json(g) for g in mesure_data['metadata']['gateways']]
    )


def get_data_from_line(line: str) -> str:
    arr: List[str] = line.split(" ")
    return arr[1]


def parse_line_to_json(line: str) -> JSONObject:
    data_str: str = get_data_from_line(line)
    return json.loads(data_str)


if __name__ == "__main__":
    path: str = sys.argv[1]
    mesures: List[Mesure] = []
    with open(path) as file:
        content: List[str] = [l.strip() for l in file.readlines()]
        for line in content:
            j = parse_line_to_json(line)
            mesures.append(parse_mesure_from_json(j))

    rssi_data_points: List[RSSIDataPoint] = []
    for m in mesures:
        rssi_data_points.append(RSSIDataPoint(
            latitude=m.latitude,
            longitude=m.longitude,
            rssi=m.gateways[0].rssi
        ))

    # print(RSSIDataPoint.get_geojson_feature_collection(rssi_data_points))
    clusters = get_clusters(
        mesures=mesures,
        nombre_min_mesures=30,
        rayon_mesure_en_metres=15
    )

    sf_clusters = filter_mesures_by_sf(mesures)
    print(sf_clusters)
