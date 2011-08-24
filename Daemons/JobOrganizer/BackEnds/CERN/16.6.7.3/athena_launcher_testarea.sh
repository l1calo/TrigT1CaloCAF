#!/bin/bash
# script to launch athena using the testarea in the l1ccalib home directory

# set up env. variables and source athena software
export STAGE_SVCCLASS=#INPUT_STAGE_SVC_CLASS#
export AtlasSetup=/afs/cern.ch/atlas/software/releases/#ATLAS_RELEASE_NOCACHE#/AtlasSetup
source $AtlasSetup/scripts/asetup.sh #ATLAS_RELEASE# --testarea /afs/cern.ch/user/l/l1ccalib/testarea --multi
#export CMTHOME=''
export CORAL_AUTH_PATH=$TestArea:$CORAL_AUTH_PATH

echo "########################################"
printenv
echo "########################################"
echo "CMTPATH: $CMTPATH"
export CMTDEBUG=1
echo "cmt show projects: `cmt show projects`" 
echo "TestArea: $TestArea"
echo "CORAL_AUTH_PATH: $CORAL_AUTH_PATH"
echo "STAGE_SVCCLASS: $STAGE_SVCCLASS"
echo "DATAPATH: $DATAPATH"
echo "pwd: `pwd`"
echo "ls -ltr: `ls -ltr`"
echo "########################################"

# copy input files to local directory
for f in `sed -n '/castor.*data/p' #JOB_OPTIONS_NAME# | sed 's/\s//g' | sed 's/[,"]//g'`
do
    rfcp $f .
done

# strip castor path from input file names in joboptions file
sed '/castor.*data/s/\"\/.*\//"/g' #JOB_OPTIONS_NAME# > jobo.py

echo "########################################"
echo "cat jobo.py"
cat jobo.py
echo "########################################"
echo "ls -ltr: `ls -lts`"
echo "########################################"

# run athena
#athena.py jobo.py | grep -v -e 'Py:Cmt            WARNING' -e 'ERROR in TileROD_Decoder ---- Unknown frag type' | tee #JOB_LOG_NAME#
athena.py jobo.py | grep -v -e 'Py:Cmt            WARNING' | tee #JOB_LOG_NAME#
#athena.py jobo.py | tee #JOB_LOG_NAME#
