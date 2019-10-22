from typing import List
from sklearn.cluster import DBSCAN

class AveragedMesure:
    def __init__(self, data_rate: str, latitude: float, longitude: float, temperature: int, humidity: int, max_gateway_rssi: float, max_gateway_snr: float):
        self.data_rate = data_rate
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.humidity = humidity
        self.max_gateway_rssi = max_gateway_rssi
        self.max_gateway_snr = max_gateway_snr


def metric(x, y)->float:
    return x.distance(y)


def get_reduced_dataset(mesures: List):
    return DBSCAN(metric=metric, eps=6, min_samples=10).fit(mesures)
