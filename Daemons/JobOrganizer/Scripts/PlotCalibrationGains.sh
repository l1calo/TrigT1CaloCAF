source /afs/cern.ch/user/l/l1ccalib/cmthome/setup.sh -tag=15.6.9,32,opt
ScriptsDir=`dirname $0`
$ScriptsDir/PlotCalibrationGains.py
python $ScriptsDir/PlotRamps.py
