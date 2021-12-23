'''
FUNCTION:
   Download S5P NO2 data from S5P-PAL Data Portal
        https://data-portal.s5p-pal.com/

UPDATES:
    Xin Zhang:
       15/12/2021: Basic

NOTES:
    Instead of using `pystac` as suggested, we can just download the links from the online json and fetch them by ourselves.
    This is actually a HACK for the world data!

    After this script is finished successfully, you will get a csv file named `s5p_portal_links.csv`.

    Option 1:
        If you wanna download all the data, you can just type one line in the terminal:
            awk '(NR>1) {print $1, $2}' s5p_portal_links.csv | xargs -n 2 -P 2 wget -O
                the number after -P is the number of files downloaded in parallel.

    Option 2:
        If you just want the data in a specific time period, you can subset the links by `subset_s5p_portal_links.py`
            and use the similar method mentioned above.
'''

import sys
import requests
import numpy as np
import pandas as pd


def get_link(search_json, total_num, step=50):
    '''Get all the search links

    Example of search link:
        https://data-portal.s5p-pal.com/cat/sentinel-5p/search?limit=10&offset=10
            limit: the number of serached products
            offset: how many products are skipped from the first one (20180501T000052)

    If we set the limit to total number of files which is over 10000, it would be an invalid request.
    So, let's create the search links by the step of 50 files, which is quick and safe.
    '''
    offsets = list(range(0, total_num, step))
    limits = np.diff(offsets+[total_num])

    search_links = []

    print('Getting all searching links ...')
    for limit, offset in zip(limits, offsets):
        search_link = search_json['links'][0]['href'].split('?')[0] + f'?limit={limit}&offset={offset}'
        search_links.append(search_link)
    print("Done. Let's fetch the download links ...")

    return search_links

def read_fields(data_json):
    '''Read useful fields'''
    filenames = [feature['id']+'.nc' for feature in data_json['features']]
    start_datetime = [feature['properties']['start_datetime'].split('+')[0] for feature in data_json['features']]
    end_datetime = [feature['properties']['end_datetime'].split('+')[0] for feature in data_json['features']]
    hashes = [feature['properties']['hash'] for feature in data_json['features']]
    links = [feature['assets']['download']['href'] for feature in data_json['features']]
    # create the DataFrame
    df = pd.DataFrame({'filename':filenames, 'link':links,
                       'start_datetime':start_datetime, 'end_datetime':end_datetime,
                       'hash': hashes})

    return df

def main():
    # read the home catalog json file
    catalog_link = 'https://data-portal.s5p-pal.com/cat/sentinel-5p/catalog.json'
    catalog = requests.get(catalog_link)

    # get the NO2 catalog json file
    no2_catalog_link = [link['href'] for link in catalog.json()['links'] if link['title'] == 'S5P_L2__NO2___'][0]
    catalog_no2 = requests.get(no2_catalog_link)

    # get the json from the search link (https://data-portal.s5p-pal.com/cat/sentinel-5p/S5P_L2__NO2___/search)
    search_json = requests.get([link['href'] for link in catalog_no2.json()['links'] if link['title'] == 'Search'][0]).json()

    # get the total number of S5P data
    total_num = search_json['context']['matched']  # you can set this to small number to test

    # get several search links by a step of 50
    search_links = get_link(search_json, total_num)

    for index, search_link in enumerate(search_links):
        print(f'Fetching download link [{index+1}/{len(search_links)}]')
        data_json = requests.get(search_link).json()
        if index == 0:
            # initialize the DataFrame
            df = read_fields(data_json)
        else:
            # append new fields
            df = pd.concat([df, read_fields(data_json)], ignore_index=True)

    # save the data to csv file
    savename = 's5p_portal_links.csv'
    print(f'Exported all links to {savename}')
    df.to_csv(savename, index=False, sep=' ')

    # check the length
    if df.shape[0] == total_num:
        print('The csv file has all the links now.')
    else:
        print('Some links are missed in the csv file ....')

if __name__ == '__main__':
    main()
