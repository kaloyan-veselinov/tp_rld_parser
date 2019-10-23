from typing import List, Dict

from numpy.core._multiarray_umath import radians
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


def get_coordinates_matrix(mesures: List['Mesure']) -> List[List[float]]:
    return [[m.latitude, m.longitude] for m in mesures]


def get_cluster_assignments(rayon_mesure_en_metres: float, nombre_min_mesures: int, coordinates: List[List[float]]) -> List[int]:
    kms_per_radian = 6371.0088
    epsilon = rayon_mesure_en_metres / 1000 / kms_per_radian
    min_samples = nombre_min_mesures
    return DBSCAN(metric='haversine', algorithm='ball_tree', eps=epsilon, min_samples=min_samples).fit(
        radians(coordinates)).labels_


def group_data(mesures: List['Mesure'], cluster_assignements: List[int])-> Dict[int, List['Mesure']]:
    data: Dict[int, List['Mesure']] = {}
    for i, mesure in enumerate(mesures):
        cluster_id: int = cluster_assignements[i]

        if cluster_id in data:
            data[cluster_id].append(mesure)
        else:
            data[cluster_id] = [mesure]

    return data


def get_clusters(rayon_mesure_en_metres: float, nombre_min_mesures: int, mesures: List['Mesure']):
    coordinates: List[List[float]] = get_coordinates_matrix(mesures)
    cluster_ids: List[int] = get_cluster_assignments(
        rayon_mesure_en_metres=rayon_mesure_en_metres,
        nombre_min_mesures=nombre_min_mesures,
        coordinates=coordinates
    )
    data = group_data(mesures=mesures, cluster_assignements=cluster_ids)
    return data
