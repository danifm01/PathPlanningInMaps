import numpy as np
from collections import defaultdict


class Dijkstra():
    def __init__(self, adjacency: dict) -> None:
        self.adjacency = adjacency
        self.reset()

    def reset(self):
        self.distances = defaultdict(lambda: np.Infinity)
        self.toExplore = defaultdict(lambda: np.Infinity)
        self.revAdjacency = defaultdict(set)
        self.visitedOrder = []

    def run(self, source: int, destiny: int):
        self.__initSearch(source)
        while self.toExplore:
            selectedNode = self.__selectNode()
            if selectedNode == destiny:
                return True
            self.__evaluateNode(selectedNode)
        return False

    def runStepByStep(self, source: int, destiny: int):
        self.__initSearch(source)
        while self.toExplore:
            selectedNode = self.__selectNode()
            yield selectedNode
            if selectedNode == destiny:
                return True
            self.__evaluateNode(selectedNode)
        return False

    def __initSearch(self, source: int):
        self.reset()
        self.distances[source] = 0
        self.toExplore[source] = 0

    def __selectNode(self):
        selectedNode = min(self.toExplore, key=self.toExplore.get)
        del(self.toExplore[selectedNode])
        self.visitedOrder.append(selectedNode)
        return selectedNode

    def __evaluateNode(self, currentNode: int):
        for node, data in self.adjacency[currentNode].items():
            self.revAdjacency[node].add(currentNode)
            dist = self.distances[currentNode] + data[0]['length']
            if dist < self.distances[node]:
                self.distances[node] = dist
                self.toExplore[node] = dist
        return False

    def getShortestPath(self, source: int, destiny: int):
        foundPath = self.run(source, destiny)
        if not foundPath:
            return False
        current = destiny
        path = [destiny]
        while current != source:
            current = min(self.revAdjacency[current], key=lambda x: self.distances.get(x, np.Infinity))
            path.append(current)
        return list(reversed(path))

if __name__  == '__main__':
    import osmnx
    import drawingUtils as draw
    import matplotlib.pyplot as plt
    region_name = 'Cebolla' 
    region = osmnx.geocoder.geocode_to_gdf(region_name, which_result=1)
    roads = osmnx.graph_from_polygon(region['geometry'][0])
    adjacency = dict(roads.adjacency())
    # source = 368238480
    # destiny = 368238483
    # source = np.random.choice(list(adjacency.keys()), 1)[0]
    source = 1865576017
    # destiny = 368238483
    destiny = 5857206372
    # for i in range(10):
    #     destiny = np.random.choice(list(adjacency.keys()), 1)[0]
    print(source)
    print(destiny)
    dijkstra = Dijkstra(adjacency)
    path = dijkstra.getShortestPath(source, destiny)
    draw.drawMap(region, show=False)
    for node in path:
        draw.drawNode(roads.nodes(data=True), node)
    plt.show()
    print(dijkstra.visitedOrder)

