'''
FUNCTION:
    Download original H8_CEReS .bz2 data

    Currently, this script only support download one kind of data in the same year.
    e.g. TIR B13 data from 06/01/2020 to 09/01/2020

LINKS:
    For more info about H8_CEReS data, please check the official website:
        http://www.cr.chiba-u.jp/databases/GEO/H8_9/FD/index.html

    For reading the file, Satpy provides the easy access using `ahi_l1b_gridded_bin` reader:
        https://satpy.readthedocs.io/en/stable/

UPDATES:
    Xin Zhang:
       01/30/2020: Basic
'''

import os
import pandas as pd
from glob import glob
from pathlib import Path
from multiprocessing import Pool
from urllib.request import urlopen

def job(url):
    file_name = str(url.split('/')[-1])
    try:
        u = urlopen(url)
        f = open(save_dir+file_name, 'wb')
        f.write(u.read())
        f.close()
        print (f'{file_name} downloaded')
    except:
        print (f'{url} does not exist')
    
def req_data(req_files):
    '''Get the missed files'''
    # get existed filenames
    exist_files = [os.path.basename(f) for f in glob(save_dir+'*.fld.geoss.bz2')]
    # get the missed filenames
    # https://stackoverflow.com/questions/41125909/python-find-elements-in-one-list-that-are-not-in-the-other
    missed_files = sorted(list(set(req_files).difference(exist_files)))
    
    return missed_files

# set data path
# I prefer download all data to the same dir to make sure they're downloaded completely
# you can sort them later using Python or anything else you like
year = '2020'
st = f'6/1/{year}' # m/d/yyyy
et = f'9/1/{year}' # m/d/yyyy
wavelengh = 'tir'
band  = '01'
save_dir = f'./data/H8_CEReS/{year}/'

# create directory

Path(save_dir).mkdir(parents=True, exist_ok=True)

# generate data period
all_dates = pd.date_range(start=st, end=et, freq='10min', closed='left')

# Because of the satellite maintenance,
# we should neglect the missing data at 02:40 and 14:40 UTC 
missing_dates = pd.date_range(start=f'{st} 02:40', end=f'{et} 02:40', freq='1D', closed='left')
missing_dates = missing_dates.union(pd.date_range(start=f'{st} 14:40', end=f'{et} 14:40', freq='1D', closed='left'))

# get the requested dates
req_dates = all_dates.drop(missing_dates)

# get wanted filenames
req_files = req_dates.strftime(f'%Y%m%d%H%M.{wavelengh}.{band}.fld.geoss.bz2') # e.g. 202007160650.tir.01.fld.geoss.bz2

# get the missed data
missed_files = req_data(req_files)

# generate urls
urls = [f'ftp://anonymous@hmwr829gr.cr.chiba-u.ac.jp/gridded/FD/V20190123/{file[:6]}/TIR/'+file for file in missed_files]

# the server allows max 5 connections
pool = Pool(4)
# download data
pool.map(job, urls)
