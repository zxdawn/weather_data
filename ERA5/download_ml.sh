#!/bin/bash -l

CODEDIR=/nuist/u/home/yinyan/xin/scratch/data/ERA5/code
DATADIR=/nuist/u/home/yinyan/xin/scratch/data/ERA5/data

# Set your python environment
export PATH=~/xin/work/anaconda3/bin:$PATH
source activate root
cd $CODEDIR

DATE1=20170419
DATE2=20170420
Nort=90
West=0
Sout=-30
East=180
YY1=`echo $DATE1 | cut -c1-4`
MM1=`echo $DATE1 | cut -c5-6`
DD1=`echo $DATE1 | cut -c7-8`
YY2=`echo $DATE2 | cut -c1-4`
MM2=`echo $DATE2 | cut -c5-6`
DD2=`echo $DATE2 | cut -c7-8`

sed -e "s/DATE1/${DATE1}/g;s/DATE2/${DATE2}/g;s/Nort/${Nort}/g;s/West/${West}/g;s/Sout/${Sout}/g;s/East/${East}/g;" GetERA5-sfc.py > GetERA5-${DATE1}-${DATE2}-sfc.py

python GetERA5-${DATE1}-${DATE2}-sfc.py

sed -e "s/DATE1/${DATE1}/g;s/DATE2/${DATE2}/g;s/Nort/${Nort}/g;s/West/${West}/g;s/Sout/${Sout}/g;s/East/${East}/g;" GetERA5-ml.py > GetERA5-${DATE1}-${DATE2}-ml.py

python GetERA5-${DATE1}-${DATE2}-ml.py

mkdir -p ${DATADIR}/$YY1

mv ERA5-${DATE1}-${DATE2}-sfc.grb ERA5-${DATE1}-${DATE2}-ml.grb ${DATADIR}/$YY1/

cd ${DATADIR}/$YY1/

echo 'write "[centre]_[dataDate]_[dataType]_[levelType]_[step].grib[edition]";' > split.rule
grib_filter split.rule ERA5-${DATE1}-${DATE2}-sfc.grb
grib_set -s deletePV=1,edition=1 ERA5-${DATE1}-${DATE2}-ml.grb ERA5-${DATE1}-${DATE2}-ml.grib1
grib_filter split.rule ERA5-${DATE1}-${DATE2}-ml.grib1

# If you want to delete original files, you can uncomment the following line.
# rm *grb

exit 0
