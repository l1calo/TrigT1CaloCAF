
export STAGE_SVCCLASS=#INPUT_STAGE_SVC_CLASS#
echo $STAGE_SVCCLASS

export ATLAS_RELEASE=#ATLAS_RELEASE#

source /afs/cern.ch/atlas/software/releases/#ATLAS_RELEASE_NOCACHE#/CMT/v1r20p20080222/mgr/setup.sh

pwd
ls -lrt
cmt config

source setup.sh -tag=#ATLAS_RELEASE#,runtime

export CMTPATH=${PWD}:${CMTPATH}

echo $CMTPATH
echo $DATAPATH

athena #JOB_OPTIONS_NAME# | tee #JOB_LOG_NAME#
