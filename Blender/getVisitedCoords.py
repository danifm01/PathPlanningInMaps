import osmnx
import osmnx.io
import json
import numpy as np

import sys
import os
path = os.path.abspath('')
sys.path.append(path)
from Dijkstra import Dijkstra
from Astar import Astar

DIJKSTRA = 0
ASTAR = 1

def getVisitedCoords(region_name, source=None, destiny=None, algorithmType=0):
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

    if algorithmType == DIJKSTRA:
        findingAlgorithm = Dijkstra(adjacency)
    elif algorithmType == ASTAR:
        nodes = dict(roads.nodes(data=True))
        findingAlgorithm = Astar(adjacency, nodes)
    else:
        raise NotImplementedError
    path = findingAlgorithm.getShortestPath(source, destiny)
    visited = findingAlgorithm.visitedOrder
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
    return notVisited, result, resultPath, source, destiny

if __name__ == '__main__':
    source = 5179960378
    destiny = 5046068653
    region_name = 'Data/Madrid_ml.osm'
    
    notVisited, result, path, source, destiny = getVisitedCoords(region_name, source, destiny, algorithmType=DIJKSTRA)
    outputName = f"{region_name.replace('.osm', '')}_Dijkstra_{source}-{destiny}.json" 
    outputNamePath = f"{region_name.replace('.osm', '')}_Dijkstra_{source}-{destiny}_path.json" 
    with open(outputName, 'w') as f:
        json.dump([result, notVisited], f)
    with open(outputNamePath, 'w') as f:
        json.dump(path, f)

    notVisited, result, path, source, destiny = getVisitedCoords(region_name, source, destiny, algorithmType=ASTAR)
    outputName = outputName.replace('Dijkstra', 'Astar')
    outputNamePath = outputNamePath.replace('Dijkstra', 'Astar')
    with open(outputName, 'w') as f:
        json.dump([result, notVisited], f)
    with open(outputNamePath, 'w') as f:
        json.dump(path, f)

