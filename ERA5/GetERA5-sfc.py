import cdsapi
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete',{
    'class':'ea',
    'date':'DATE1/to/DATE2',
    'area':'Nort/West/Sout/East',
    'expver':'1',
    'levtype':'sfc',
   'param':'msl/sp/skt/2t/10u/10v/2d/z/lsm/sst/ci/sd/stl1/stl2/stl3/stl4/swvl1/swvl2/swvl3/swvl4',
    'stream':'oper',
    'time':'00:00:00/03:00:00/06:00:00/09:00:00/12:00:00/15:00:00/18:00:00/21:00:00',
    'type':'an',
    'grid':"0.25/0.25",
},'ERA5-DATE1-DATE2-sfc.grb')
