'''
FUNCTION:
   Subset the links downloaded by `fetch_s5p_portal_links.py` during specific time period.

UPDATES:
    Xin Zhang:
       15/12/2021: Basic
'''

import pandas as pd

# set the start time and end time
st = "2019-07-03"  # "yyyy-mm-dd HH:MM:SS"
et = "2019-07-31"

# read the file of download info
file_links = './s5p_portal_links.csv'
df = pd.read_csv(file_links, parse_dates=['start_datetime'], sep=' ')
df = df.set_index(['start_datetime'])

# subset the DataFrame to the selected date range
df = df.loc[st:et]

# export the subset to a new csv named "{st}_{et}.csv"
savename = pd.to_datetime(st).strftime('%Y%m%d_') + pd.to_datetime(et).strftime('%Y%m%d.csv')
print(f'The links from "{file_links}" are subsetted and saved into "{savename}"')
df.to_csv(savename, index=False, sep=' ')
