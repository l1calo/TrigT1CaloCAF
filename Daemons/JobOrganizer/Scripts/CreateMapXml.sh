#!/bin/sh

# Create l1calomap xml file from energy scan results.
# For the moment it is assumed these are in the file
# energyscanresults.sqlite in the current directory.

#tdaqver=04-00-01
tdaqver=05-00-01
#export CMTCONFIG=i686-slc5-gcc43-opt
export CMTCONFIG=i686-slc6-gcc47-opt
tdaqdirafs=/afs/cern.ch/atlas/project/tdaq
source ${tdaqdirafs}/inst/tdaq/tdaq-${tdaqver}/installed/setup.sh
source ${tdaqdirafs}/level1/calo/rel/nightly/installed/setup/setup.sh

dbconn='sqlite://;schema=energyscanresults.sqlite;dbname=L1CALO'
folder='/TRIGGER/L1Calo/V1/Results/EnergyScanResults'
attrib='Chi2:0:200,ErrorCode:1,Ndf:0:9,Offset:-1:1,Slope:0.6:1.5'
dumpfolder.py -d "${dbconn}" -l PpmMcmChan -a "${attrib}" ${folder}
