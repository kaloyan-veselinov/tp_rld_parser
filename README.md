# tp_rld_parser

## Utilisation

```bash
python3 parser.py < chemin vers le fichiers de mesures >
```

## Types de cartes générées

Les cartes sont générées dans un dossier `maps` à la racine du projet.

- `gateways.geojson` correspond à une carte des gateways identifiées ;
- `clusters.geojson` correspond à une carte des regroupements des mesures par position ; ces regroupements sont ensuite utilisés pour du moyennage ;
- `GW/{gateway_id}_coverage.geojson` correspond à une carte de couverture pour une gateway donnée ;
- `SF/{sf}_coverage.geojson` correspond à une carte de couverture pour chaque SF, en utilisant la puissance maximale observée sur toutes les gateways.

## Types de traitements

### Clustering

Pour identifier les différentes positions de mesure, nous avons utilisé un clustering par densité avec DBSCAN.

### Filtrage

Sur chaque cluster, nous avons ensuite appliqué différents filtrages (mesures par SF, par GW, etc.), selon la carte générée.

### Moyennage

Une fois le clustering et le filtrage réalisés, les données sont moyennées pour construire la carte finale. 

## Références

 - [Clustering avec DBSCAN - stackoverflow](https://stackoverflow.com/questions/24762435/clustering-geo-location-coordinates-lat-long-pairs-using-kmeans-algorithm-with)
 - [Documentation de l'implémentation de DBSCAN de scikit](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)
 