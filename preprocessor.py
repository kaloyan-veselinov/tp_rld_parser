from copy import copy
from typing import List, Dict

from numpy.core._multiarray_umath import radians
from sklearn.cluster import DBSCAN


def filter_mesures_by_sf(mesures: List['Mesure']) -> Dict[str, List['Mesure']]:
    mesures_by_sf: Dict[str, List['Mesure']] = {}
    for m in mesures:
        if m.data_rate in mesures_by_sf:
            mesures_by_sf[m.data_rate].append(m)
        else:
            mesures_by_sf[m.data_rate] = [m]
    return mesures_by_sf


def filter_mesures_by_gateway(mesures: List['Mesure']) -> Dict[str, List['Mesure']]:
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


def get_cluster_assignments(rayon_mesure_en_metres: float, nombre_min_mesures: int, coordinates: List[List[float]]) -> \
List[int]:
    kms_per_radian = 6371.0088
    epsilon = rayon_mesure_en_metres / 1000 / kms_per_radian
    min_samples = nombre_min_mesures
    return DBSCAN(metric='haversine', algorithm='ball_tree', eps=epsilon, min_samples=min_samples).fit(
        radians(coordinates)).labels_


def group_data(mesures: List['Mesure'], cluster_assignements: List[int]) -> Dict[int, List['Mesure']]:
    data: Dict[int, List['Mesure']] = {}
    for i, mesure in enumerate(mesures):
        cluster_id: int = cluster_assignements[i]

        if cluster_id in data:
            data[cluster_id].append(mesure)
        else:
            data[cluster_id] = [mesure]

    return data


def get_clusters(rayon_mesure_en_metres: float, nombre_min_mesures: int, mesures: List['Mesure']) -> Dict[int, List['Mesure']]:
    coordinates: List[List[float]] = get_coordinates_matrix(mesures)
    cluster_ids: List[int] = get_cluster_assignments(
        rayon_mesure_en_metres=rayon_mesure_en_metres,
        nombre_min_mesures=nombre_min_mesures,
        coordinates=coordinates
    )
    data = group_data(mesures=mesures, cluster_assignements=cluster_ids)
    return data
