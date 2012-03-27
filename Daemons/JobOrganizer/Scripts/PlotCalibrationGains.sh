export AtlasSetup=/afs/cern.ch/atlas/software/releases/17.1.2/AtlasSetup
source $AtlasSetup/scripts/asetup.sh 17.1.2.1,32
ScriptsDir=`dirname $0`
$ScriptsDir/PlotCalibrationGains.py
python $ScriptsDir/PlotRamps.py
