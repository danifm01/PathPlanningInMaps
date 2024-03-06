import osmnx
import osmnx.io
import json
import numpy as np

import sys
import os
path = os.path.abspath('')
sys.path.append(path)
from Dijkstra import Dijkstra


def getVisitedCoords(region_name, source=None, destiny=None):
    if region_name.endswith('.osm'):
        # roads = osmnx.graph_from_xml(region_name)
        roads = osmnx.io.load_graphml(region_name)
    else:
        
        region = osmnx.geocoder.geocode_to_gdf(region_name, which_result=1)
        roads = osmnx.graph_from_polygon(region['geometry'][0])
    adjacency = dict(roads.adjacency())

    if source is None:
        source = np.random.choice(list(adjacency.keys()), 1)[0]
    if destiny is None:
        destiny = np.random.choice(list(adjacency.keys()), 1)[0]

    dijkstra = Dijkstra(adjacency)
    path = dijkstra.getShortestPath(source, destiny)
    visited = dijkstra.visitedOrder
    notVisited = []
    setVisited = set(visited)
    for node in roads.nodes:
        if not node in setVisited:
            aux = roads.nodes[node]
            notVisited.append((aux['x'], aux['y']))
    result = []
    for v in visited:
        aux = roads.nodes[v]
        result.append((aux['x'], aux['y']))
    resultPath = []
    for v in path:
        aux = roads.nodes[v]
        resultPath.append((aux['x'], aux['y']))
    return notVisited, result, resultPath

if __name__ == '__main__':
    # region_name = 'Cebolla' 
    # source = 1865576017
    # destiny = 5857206372
    # notVisited, result, _ = getVisitedCoords(region_name, source, destiny)

    region_name = 'Data/Madrid_ml.osm'
    notVisited, result, path = getVisitedCoords(region_name)
    outputName = f"{region_name.replace('.osm', '')}.json" 
    outputNamePath = f"{region_name.replace('.osm', '')}_path.json" 
    with open(outputName, 'w') as f:
        json.dump([result, notVisited], f)
    with open(outputNamePath, 'w') as f:
        json.dump(path, f)

