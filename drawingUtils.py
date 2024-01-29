import osmnx
import matplotlib.pyplot as plt

def drawMap(region, show=True):
    roads = osmnx.graph_from_polygon(region['geometry'][0])
    rivers = osmnx.features_from_polygon(region['geometry'][0], tags = {'waterway': 'river'})

    ax = region.plot(facecolor = '#494D4D', figsize=(85,85))
    ax.set_facecolor('#2C2E2E')
    rivers.plot(edgecolor = '#67A0C3',
                linewidth = 5,
                linestyle = '-',
                ax = ax)
    fig, ax = osmnx.plot_graph(roads,
                edge_color = 'white',
                node_color = 'blue',
                edge_linewidth=1,
                node_size = 15,
                ax=ax,
                show=False)
    ax.grid('on', which='major', axis='x', color = '#99A2A2')
    ax.grid('on', which='major', axis='y', color = '#99A2A2')
    ax.get_xaxis().set_visible(True)
    ax.get_yaxis().set_visible(True)
    if show:
        plt.show()

def drawNode(nodes, nodeNum):
    x = nodes[nodeNum]['x']
    y = nodes[nodeNum]['y']
    plt.plot(x, y, marker='o', markersize=10, markerfacecolor="red")
