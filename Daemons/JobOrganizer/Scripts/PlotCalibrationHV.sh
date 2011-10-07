export AtlasSetup=/afs/cern.ch/atlas/software/releases/17.0.3/AtlasSetup
source $AtlasSetup/scripts/asetup.sh 17.0.3.4,32
#source /afs/cern.ch/user/l/l1ccalib/cmthome/setup.sh -tag=15.6.9,32,opt
ScriptsDir=`dirname $0`
python $ScriptsDir/PlotCalibrationHV.py -f hvcorrections.sqlite
