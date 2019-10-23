from statistics import mean, median
from typing import List, Dict

from preprocessor import filter_mesures_by_gateway, get_clusters


class Gateway:
    def __init__(self, gw_id: str, latitude: float, longitude: float):
        self.gw_id = gw_id
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f'id: {self.gw_id} lat: {self.latitude} long: {self.longitude}'

    def __repr__(self):
        return self.__str__()


class AveragedMesure:
    def __init__(self, mesures: List['Mesure']):
        self.latitude = median(m.latitude for m in mesures)
        self.longitude = median(m.longitude for m in mesures)
        self.temperature = median(m.temperature for m in mesures)
        self.humidity = median(m.humidity for m in mesures)
        self.max_gateway_rssi = mean(m.gateways[0].rssi for m in mesures)
        self.max_gateway_snr = mean(m.gateways[0].snr for m in mesures)

    def __str__(self):
        return f'latitude: {self.latitude} longitude: {self.longitude} temperature: {self.temperature} humidity: {self.humidity} max_rssi: {self.max_gateway_rssi} max_snr: {self.max_gateway_snr}'


def get_gateways(mesures: List['Mesure']) -> Dict[str, Gateway]:
    gateways: Dict[str, Gateway] = {}
    for mesure in mesures:
        for mesure_gw in mesure.gateways:
            if mesure_gw.id not in gateways:
                if mesure_gw.latitude and mesure_gw.longitude:
                    gateways[mesure_gw.id] = Gateway(
                        gw_id=mesure_gw.id,
                        latitude=mesure_gw.latitude,
                        longitude=mesure_gw.longitude
                    )
    return gateways


def get_gateways_coverage(mesures: List['Mesure']) -> Dict[str, List[AveragedMesure]]:
    gateways_coverage: Dict[str, List[AveragedMesure]] = {}
    mesures_by_gw: Dict[str, List['Mesure']] = filter_mesures_by_gateway(mesures)

    for gw_id, m in mesures_by_gw.items():
        clustered_data = get_clusters(
            mesures=m,
            nombre_min_mesures=10,
            rayon_mesure_en_metres=30
        )
        for cluster_id, cluster_mesures in clustered_data.items():
            if cluster_id != -1:
                average_mesure = AveragedMesure(mesures=cluster_mesures)
                if gw_id in gateways_coverage:
                    gateways_coverage[gw_id].append(average_mesure)
                else:
                    gateways_coverage[gw_id] = [average_mesure]

    return gateways_coverage
