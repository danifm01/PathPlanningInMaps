import numpy as np
from collections import defaultdict
import geopy.distance
from tqdm import tqdm


class Astar():
    def __init__(self, adjacency: dict, nodes: dict) -> None:
        self.adjacency = adjacency
        self.nodes = nodes
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
            currentF = currentG + self.__getDistanceToDestiny(node)
            if currentF < self.f[node]:
                self.g[node] = currentG
                self.f[node] = currentF 
                self.toExplore[node] = currentF
        return False

    def __getH(self, node):
        return self.__getDistanceToDestiny(node)

    def __getDistanceToDestiny(self, node):
        coord1 = (self.nodes[node]['y'], self.nodes[node]['x'])
        coord2 = (self.nodes[self.destiny]['y'], self.nodes[self.destiny]['x'])
        distance = geopy.distance.geodesic(coord1, coord2).m 
        return distance / 1 

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
    print(source)
    print(destiny)
    astar = Astar(adjacency, nodes)
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
