import math
import bpy
import json
import mathutils
import numpy as np
import sys
sys.path.append('C:\\Users\\danfe\\AppData\\Roaming\\Python\\Python310\\Scripts'+ '\\..\\site-packages')
from tqdm import tqdm

FILEPATH = 'test3.json'
FILEPATH = 'Data/Madrid_ml.json'

class TransverseMercator:
    radius = 6378137.

    def __init__(self, **kwargs):
        # setting default values
        self.lat = 0. # in degrees
        self.lon = 0. # in degrees
        self.k = 1. # scale factor
        
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        self.latInRadians = math.radians(self.lat)

    def fromGeographic(self, lat, lon):
        lat = math.radians(lat)
        lon = math.radians(lon-self.lon)
        B = math.sin(lon) * math.cos(lat)
        x = 0.5 * self.k * self.radius * math.log((1.+B)/(1.-B))
        y = self.k * self.radius * ( math.atan(math.tan(lat)/math.cos(lon)) - self.latInRadians )
        return (x, y, 0.)

    def toGeographic(self, x, y):
        x = x/(self.k * self.radius)
        y = y/(self.k * self.radius)
        D = y + self.latInRadians
        lon = math.atan(math.sinh(x)/math.cos(D))
        lat = math.asin(math.sin(D)/math.cosh(x))

        lon = self.lon + math.degrees(lon)
        lat = math.degrees(lat)
        return (lat, lon)

lat = bpy.context.scene['lat']
lon = bpy.context.scene['lon']
converter = TransverseMercator(lat=lat, lon=lon)
with open(FILEPATH, 'r') as f:
    data = json.load(f)
with open(FILEPATH.replace('.json', '_path.json'), 'r') as f:
    shortestPath = json.load(f)
visited = data[0]
notVisited = data[1]
nodes = visited + notVisited
maxVisitedIndex = len(visited)

tree = mathutils.kdtree.KDTree(len(nodes))
for i, v in enumerate(tqdm(nodes)):
    coord = converter.fromGeographic(v[1], v[0])
    tree.insert(coord, i)
tree.balance()

roads = bpy.context.active_object
roads.data.attributes.new('visited', 'INT', 'POINT')
roads.data.attributes.new('isShortestPath', 'INT', 'POINT')
testResult = []
for i, vertex in enumerate(tqdm(roads.data.vertices)):
    co, index, dist = tree.find(vertex.co)
    if index >= maxVisitedIndex:
        index = -1
    roads.data.vertices.data.attributes['visited'].data[i].value = index
    if nodes[index] in shortestPath:
        roads.data.vertices.data.attributes['isShortestPath'].data[i].value = 1
    else:
        roads.data.vertices.data.attributes['isShortestPath'].data[i].value = 0

print('************************END*********************************')