import json
import sys
from json.decoder import JSONObject
from typing import List


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
    def __init__(self, data_rate: str, coding_rate: str, latitude: float, longitude: float,
                 temperature: int, humidity: int, gateways: List[Gateway]):
        self.data_rate = data_rate
        self.coding_rate = coding_rate
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.humidity = humidity
        self.gateways = gateways

    def __str__(self):
        return f'data_rate: {self.data_rate} latitude: {self.latitude} longitude: {self.longitude} temperature: {self.temperature} humidity: {self.humidity} gateways: {self.gateways}'


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
        data_rate=mesure_data['metadata']['data_rate'],
        coding_rate=mesure_data['metadata']['coding_rate'],
        latitude=mesure_data['payload_fields']['latitude'],
        longitude=mesure_data['payload_fields']['longitude'],
        temperature=mesure_data['payload_fields']['latitude'],
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
    with open(path) as file:
        content: List[str] = [l.strip() for l in file.readlines()]
        for line in content:
            j = parse_line_to_json(line)
            m: Mesure = parse_mesure_from_json(j)
            print(m)
