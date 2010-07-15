export STAGE_SVCCLASS=#INPUT_STAGE_SVC_CLASS#
echo $STAGE_SVCCLASS

export ATLAS_RELEASE=#ATLAS_RELEASE_NOCACHE#

source /afs/cern.ch/atlas/software/releases/#ATLAS_RELEASE_NOCACHE#/CMT/v1r20p20090520/mgr/setup.sh

pwd
ls -lrt

# somehow things crash if cmt is setup in the same directory athena runs
mkdir cmthome
mv requirements cmthome
cd cmthome

cmt config
source setup.sh -tag=$ATLAS_RELEASE,runtime,noTest

echo $DATAPATH

cd ..

# copy input files to local directory
for f in `sed -n '/castor.*data/p' #JOB_OPTIONS_NAME# | sed 's/\s//g' | sed 's/[,"]//g'`
do
    rfcp $f .
done

# change input file names in joboptions file
sed '/castor.*data/s/\"\/.*\//"/g' #JOB_OPTIONS_NAME# > jobo.py

cat jobo.py

ls -lts

athena.py jobo.py | tee #JOB_LOG_NAME#
