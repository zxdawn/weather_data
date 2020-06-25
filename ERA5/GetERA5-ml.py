import cdsapi
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete',{
    'class':'ea',
    'date':'DATE1/to/DATE2',
    'area':'Nort/West/Sout/East',
    'expver':'1',
    'levelist': '1/to/137',
    'levtype':'ml',
    'param':'129/130/131/132/133/152',
    'stream':'oper',
    'time':'00:00:00/03:00:00/06:00:00/09:00:00/12:00:00/15:00:00/18:00:00/21:00:00',
    'type':'an',
    'grid':"0.25/0.25",
},'ERA5-DATE1-DATE2-ml.grb')
