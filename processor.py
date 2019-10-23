from copy import copy
from statistics import mean, median
from typing import List, Dict

from numpy.core._multiarray_umath import radians
from sklearn.cluster import DBSCAN


class Gateway:
    def __init__(self, id: str, latitude: float, longitude: float):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f'id: {self.id} lat: {self.latitude} long: {self.longitude}'

    def __repr__(self):
        return self.__str__()


class AveragedMesure:
    def __init__(self, mesures: List['Mesure']):
        self.latitude = mean(m.latitude for m in mesures)
        self.longitude = mean(m.longitude for m in mesures)
        self.temperature = median(m.temperature for m in mesures)
        self.humidity = median(m.humidity for m in mesures)
        self.max_gateway_rssi = mean(m.gateways[0].rssi for m in mesures)
        self.max_gateway_snr = mean(m.gateways[0].snr for m in mesures)

    def __str__(self):
        return f'latitude: {self.latitude} longitude: {self.longitude} temperature: {self.temperature} humidity: {self.humidity} max_rssi: {self.max_gateway_rssi} max_snr: {self.max_gateway_snr}'


def filter_mesures_by_sf(mesures: List['Mesure'])->Dict[str, List['Mesure']]:
    mesures_by_sf: Dict[str, List['Mesure']] = {}
    for m in mesures:
        if m.data_rate in mesures_by_sf:
            mesures_by_sf[m.data_rate].append(m)
        else:
            mesures_by_sf[m.data_rate] = [m]
    return mesures_by_sf


def get_gateways(mesures: List['Mesure'])->Dict[str, Gateway]:
    gateways: Dict[str, Gateway] = {}
    for mesure in mesures:
        for mesure_gw in mesure.gateways:
            if mesure_gw.id not in gateways:
                if mesure_gw.latitude and mesure_gw.longitude:
                    gateways[mesure_gw.id] = Gateway(
                        id=mesure_gw.id,
                        latitude=mesure_gw.latitude,
                        longitude=mesure_gw.longitude
                    )
    return gateways


def filter_mesures_by_gateway(mesures: List['Mesure'])->Dict[str, List['Mesure']]:
    mesures_by_gateway: Dict[str, List['Mesure']] = {}
    for mesure in mesures:
        for mesure_gw in mesure.gateways:
            mesure_copy = copy(mesure)
            mesure_copy.gateways = [gwm for gwm in mesure.gateways if gwm.id == mesure_gw.id]

            if mesure_gw.id in mesures_by_gateway:
                mesures_by_gateway[mesure_gw.id].append(mesure_copy)
            else:
                mesures_by_gateway[mesure_gw.id] = [mesure_copy]

    return mesures_by_gateway


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
