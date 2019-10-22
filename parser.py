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


class Mesure:
    def __init__(self, device_id: str, data_rate: str, coding_rate: str, latitude: float, longitude: float, temperature: int, humidity: int, gateways: List[Gateway]):
        self.device_id = device_id
        self.data_rate = data_rate
        self.coding_rate = coding_rate
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.humidity = humidity
        self.gateways = gateways


def get_data_from_line(line: str)->str:
    arr = line.split(" ")
    return arr[1]


def parse_line_to_json(line: str)->JSONObject:
    data_str: str = get_data_from_line(line)
    return json.loads(data_str)


if __name__ == "__main__":
    path = sys.argv[1]
    with open(path) as file:
        content = [l.strip() for l in file.readlines()]
        for line in content:
            print(parse_line_to_json(line))
