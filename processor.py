from statistics import mean, median
from typing import List, Dict

from preprocessor import filter_mesures_by_gateway, filter_mesures_by_sf


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
        self.max_gateway_rssi = round(mean(m.gateways[0].rssi for m in mesures))
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


def get_gateways_coverage(clustered_data: Dict[int, List['Mesure']]) -> Dict[str, List[AveragedMesure]]:
    gateways_coverage: Dict[str, List[AveragedMesure]] = {}

    for cluster_id, cluster_mesures in clustered_data.items():
        if cluster_id != -1:
            for gw, gw_mesures in filter_mesures_by_gateway(cluster_mesures).items():
                average_mesure = AveragedMesure(mesures=gw_mesures)
                if gw in gateways_coverage:
                    gateways_coverage[gw].append(average_mesure)
                else:
                    gateways_coverage[gw] = [average_mesure]

    return gateways_coverage


def get_coverage_by_sf(clustered_data: Dict[int, List['Mesure']]) -> Dict[str, List[AveragedMesure]]:
    coverage_by_sf: Dict[str, List[AveragedMesure]] = {}
    for cluster_id, cluster_mesures in clustered_data.items():
        if cluster_id != -1:
            for sf, sf_mesures in filter_mesures_by_sf(cluster_mesures).items():
                average_mesure = AveragedMesure(mesures=sf_mesures)
                if sf in coverage_by_sf:
                    coverage_by_sf[sf].append(average_mesure)
                else:
                    coverage_by_sf[sf] = [average_mesure]

    return coverage_by_sf
