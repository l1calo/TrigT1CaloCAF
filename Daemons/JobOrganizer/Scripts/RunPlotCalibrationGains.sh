export AtlasSetup=/afs/cern.ch/atlas/software/releases/17.2.8/AtlasSetup
source $AtlasSetup/scripts/asetup.sh 17.2.8.7,32 --testarea /afs/cern.ch/user/l/l1ccalib/testarea --multi
get_files COOLIdDump.txt
ScriptsDir=`dirname $0`
$ScriptsDir/RunPlotCalibrationGains.py
