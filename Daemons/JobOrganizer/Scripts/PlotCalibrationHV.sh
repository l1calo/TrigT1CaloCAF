export AtlasSetup=/afs/cern.ch/atlas/software/releases/17.2.0/AtlasSetup
source $AtlasSetup/scripts/asetup.sh 17.2.0.2,32
ScriptsDir=`dirname $0`
python $ScriptsDir/PlotCalibrationHV.py -f hvcorrections.sqlite
