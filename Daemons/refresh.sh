export DAEMONDIR=/afs/cern.ch/user/l/l1ccalib/testarea/15.2.0/Trigger/TrigT1/TrigT1CaloCAF/Daemons
source $DAEMONDIR/setup.sh

cd $DAEMONDIR/RunsProvider
$DAEMONDIR/RunsProvider/RunsProviderDaemon.py restart

cd $DAEMONDIR/JobOrganizer
$DAEMONDIR/JobOrganizer/JobOrganizerDaemon.py restart

cd $DAEMONDIR/W0Monitor
$DAEMONDIR/W0Monitor/W0MonitorDaemon.py restart
