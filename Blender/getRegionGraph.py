import osmnx
import osmnx.io

region_name='Madrid'

region = osmnx.geocoder.geocode_to_gdf(region_name, which_result=1)
roads = osmnx.graph_from_polygon(region['geometry'][0])
adjacency = dict(roads.adjacency())
osmnx.save_graph_xml(roads, f'Data/{region_name}.osm')
osmnx.io.save_graphml(roads, f'Data/{region_name}_ml.osm')