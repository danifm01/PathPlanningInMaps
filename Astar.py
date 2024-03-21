import numpy as np
from collections import defaultdict
import geopy.distance
from tqdm import tqdm

ASTAR_EUCLIDEAN = 1
ASTAR_MANHATTAN = 2
ASTAR_CHEBISHEB = 3
ASTAR_GREEDY = 4

class Astar():
    def __init__(self, adjacency: dict, nodes: dict, heuristicType: int=ASTAR_EUCLIDEAN) -> None:
        self.adjacency = adjacency
        self.nodes = nodes
        self.heuristic = heuristicType
        self.reset()

    def reset(self):
        # TODO: Add list of closed nodes
        self.f = defaultdict(lambda: np.Infinity)
        self.g = defaultdict(lambda: np.Infinity)
        self.toExplore = defaultdict(lambda: np.Infinity)
        self.revAdjacency = defaultdict(set)
        self.visitedOrder = []
        self.visited = defaultdict(lambda: 0)
        self.destiny = -1

    def run(self, source: int, destiny: int):
        self.__initSearch(source, destiny)
        pbar = tqdm()
        while self.toExplore:
            pbar.update()
            selectedNode = self.__selectNode()
            if selectedNode == destiny:
                return True
            self.__evaluateNode(selectedNode)
        pbar.close()
        return False

    def runStepByStep(self, source: int, destiny: int):
        self.__initSearch(source, destiny)
        while self.toExplore:
            selectedNode = self.__selectNode()
            yield selectedNode
            if selectedNode == destiny:
                return True
            self.__evaluateNode(selectedNode)
        return False

    def __initSearch(self, source: int, destiny: int):
        self.reset()
        self.destiny = destiny
        self.g[source] = 0
        self.f[source] = 0 + self.__getH(source)
        self.toExplore[source] = 0

    def __selectNode(self):
        selectedNode = min(self.toExplore, key=self.toExplore.get)
        del(self.toExplore[selectedNode])
        self.visitedOrder.append(selectedNode)
        return selectedNode

    def __evaluateNode(self, currentNode: int):
        for node, data in self.adjacency[currentNode].items():
            self.revAdjacency[node].add(currentNode)
            currentG = self.g[currentNode] + data[0]['length'] 
            if self.heuristic == ASTAR_GREEDY:
                currentF = self.__getDistanceToDestiny(node)
            else:
                currentF = currentG + self.__getH(node)
            if currentF < self.f[node]:
                self.g[node] = currentG
                self.f[node] = currentF 
                self.toExplore[node] = currentF
        return False

    def __getH(self, node):
        return {ASTAR_EUCLIDEAN: self.__getDistanceToDestiny(node),
                ASTAR_MANHATTAN: self.__getManhattanDistance(node),
                ASTAR_CHEBISHEB: self.__getChebishebDistance(node),
                ASTAR_GREEDY: self.__getDistanceToDestiny(node)}[self.heuristic]

    def __getDistanceToDestiny(self, node):
        coord1 = (self.nodes[node]['y'], self.nodes[node]['x'])
        coord2 = (self.nodes[self.destiny]['y'], self.nodes[self.destiny]['x'])
        distance = geopy.distance.geodesic(coord1, coord2).m 
        return distance

    def __getManhattanDistance(self, node):
        coord1 = (self.nodes[node]['y'], self.nodes[node]['x'])
        coord2 = (self.nodes[self.destiny]['y'], self.nodes[node]['x'])
        distance1 = geopy.distance.geodesic(coord1, coord2).m 
        coord1 = (self.nodes[node]['y'], self.nodes[node]['x'])
        coord2 = (self.nodes[node]['y'], self.nodes[self.destiny]['x'])
        distance2 = geopy.distance.geodesic(coord1, coord2).m 
        return distance1 + distance2 

    def __getChebishebDistance(self, node):
        coord1 = (self.nodes[node]['y'], self.nodes[node]['x'])
        coord2 = (self.nodes[self.destiny]['y'], self.nodes[node]['x'])
        distance1 = geopy.distance.geodesic(coord1, coord2).m 
        coord1 = (self.nodes[node]['y'], self.nodes[node]['x'])
        coord2 = (self.nodes[node]['y'], self.nodes[self.destiny]['x'])
        distance2 = geopy.distance.geodesic(coord1, coord2).m 
        return min(distance1, distance2)

    def getShortestPath(self, source: int, destiny: int):
        foundPath = self.run(source, destiny)
        if not foundPath:
            return False
        current = destiny
        path = [destiny]
        while current != source:
            current = min(self.revAdjacency[current], key=lambda x: self.g.get(x, np.Infinity))
            path.append(current)
        return list(reversed(path))

if __name__  == '__main__':
    import osmnx
    import drawingUtils as draw
    import matplotlib.pyplot as plt
    region_name = 'Cebolla' 
    region = osmnx.geocoder.geocode_to_gdf(region_name, which_result=1)
    roads = osmnx.graph_from_polygon(region['geometry'][0])
    nodes = dict(roads.nodes(data=True))
    adjacency = dict(roads.adjacency())
    # source = np.random.choice(list(adjacency.keys()), 1)[0]
    source = 1865576017
    # destiny = 368238483
    destiny = 5857206372
    # for i in range(10):
    #     destiny = np.random.choice(list(adjacency.keys()), 1)[0]
    source = 1629096132
    destiny = 4679051993
    print(source)
    print(destiny)
    astar = Astar(adjacency, nodes, 4)
    path = astar.getShortestPath(source, destiny)
    draw.drawMap(region, show=False)
    for node in path:
        draw.drawNode(roads.nodes(data=True), node)
    plt.show()
    draw.drawMap(region, show=False)
    for node in astar.visitedOrder:
        draw.drawNode(roads.nodes(data=True), node)
    plt.show()
    print(astar.visitedOrder)
