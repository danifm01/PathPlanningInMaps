import osmnx
import matplotlib.pyplot as plt
import drawingUtils as draw

def main():
    REGION_NAME = 'Madrid' 
    region = osmnx.geocoder.geocode_to_gdf(REGION_NAME, which_result=1)
    draw.drawMap(region)

if __name__ == '__main__':
    main()
