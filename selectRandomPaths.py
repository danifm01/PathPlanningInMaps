# %%
import osmnx
import drawingUtils as draw
import matplotlib.pyplot as plt
from Astar import Astar
import numpy as np
import os


regionName = 'Pekin'
savePath = f'MapImages/{regionName}'
os.makedirs(savePath, exist_ok=True)

# region = osmnx.geocoder.geocode_to_gdf(regionName, which_result=1)
region = osmnx.geocoder.geocode_to_gdf(regionName)
roads = osmnx.graph_from_polygon(region['geometry'][0])
adjacency = dict(roads.adjacency())
nodes = dict(roads.nodes(data=True))
# %%
N = 40
for i in range(N):
    source = np.random.choice(list(adjacency.keys()), 1)[0]
    destiny = np.random.choice(list(adjacency.keys()), 1)[0]
    print(source)
    print(destiny)

    astar = Astar(adjacency, nodes, 4)
    path = astar.getShortestPath(source, destiny)
    osmnx.plot_graph(roads,
                # edge_color = 'white',
                # node_color = 'blue',
                figsize=(20, 20),
                edge_linewidth=0,
                node_size = 1,
                show=False)
    for node in path:
        draw.drawNode(roads.nodes(data=True), node)
    title = f'{source}-{destiny}'
    plt.title(title)
    plt.savefig(os.path.join(savePath, title) + '.png')
    plt.show()
# %%
