
export STAGE_SVCCLASS=#INPUT_STAGE_SVC_CLASS#
echo $STAGE_SVCCLASS

export ATLAS_RELEASE=#ATLAS_RELEASE#

source /afs/cern.ch/atlas/software/releases/#ATLAS_RELEASE_NOCACHE#/CMT/v1r20p20090520/mgr/setup.sh

pwd
ls -lrt

# somehow things crash if cmt is setup in the same directory athena runs
mkdir cmthome
mv requirements cmthome
cd cmthome

cmt config
source setup.sh -tag=#ATLAS_RELEASE#,runtime,noTest

export CMTPATH=${PWD}:${CMTPATH}

echo $CMTPATH
echo $DATAPATH

cd ..

athena.py #JOB_OPTIONS_NAME# | tee #JOB_LOG_NAME#
