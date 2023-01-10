'''
FUNCTION:
   Download the geometry of S5P NO2 data from S5P-PAL Data Portal
        https://data-portal.s5p-pal.com/

UPDATES:
    Xin Zhang:
       10/101/2023: Basic
'''

import requests
import pandas as pd
import geopandas as gpd
from fetch_s5p_portal_links import all_links
from shapely.geometry import Polygon, MultiPolygon

world_geo = [[-180.0, -90.0],
             [180.0, -90.0],
             [180.0, 90.0],
             [-180.0, 90.0],
             [-180.0, -90.0]]

def read_geometry(coordinates):
    '''Generate the plygon or multipolygon for geometry'''
    geometry = MultiPolygon([Polygon(r[0]) if len(r)==1 else Polygon(r) for r in coordinates])
    # sometime the polygon is wrong
    #   https://github.com/zxdawn/weather_data/issues/4
    if (coordinates[0] == world_geo) & (len(coordinates)==2):
        geometry = geometry.geoms[0].difference(geometry.geoms[1])
    elif (coordinates[0] == world_geo) & (len(coordinates)!=2):
        print(f'!'*20, 'The geometry is wrong. Please check the coords: {coordinates}')

    return geometry

def read_fields(data_json):
    '''Read useful fields'''
    filenames = [feature['id']+'.nc' for feature in data_json['features']]
    geometry = [read_geometry(feature['geometry']['coordinates']) for feature in data_json['features']]


    # create the Geo DataFrame
    gdf = gpd.GeoDataFrame({'filename':filenames, 'geometry': geometry})

    return gdf


def main():
    search_links, total_num = all_links()
    for index, search_link in enumerate(search_links):
        print(f'Fetching geometry [{index+1}/{len(search_links)}]')
        data_json = requests.get(search_link).json()
        if index == 0:
            # initialize the DataFrame
            gdf = read_fields(data_json)
        else:
            # append new fields
            gdf = pd.concat([gdf, read_fields(data_json)], ignore_index=True)

    # save the data to shp file
    savename = 's5p_swaths.shp'
    print(f'Exported all geometries to {savename}')
    gdf.to_file(savename, index=False)

    # check the length
    if gdf.shape[0] == total_num:
        print('The shp file has all the geometries now.')
    else:
        print('Some geometries are missed in the shp file ....')


if __name__ == '__main__':
    main()

