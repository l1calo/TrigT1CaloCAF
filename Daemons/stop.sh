export DAEMONDIR=/afs/cern.ch/user/l/l1ccalib/testarea/15.2.0/Trigger/TrigT1/TrigT1CaloCAF/Daemons
source $DAEMONDIR/setup.sh

cd $DAEMONDIR/RunsProvider
$DAEMONDIR/RunsProvider/RunsProviderDaemon.py stop

cd $DAEMONDIR/JobOrganizer
$DAEMONDIR/JobOrganizer/JobOrganizerDaemon.py stop

cd $DAEMONDIR/W0Monitor
$DAEMONDIR/W0Monitor/W0MonitorDaemon.py stop
