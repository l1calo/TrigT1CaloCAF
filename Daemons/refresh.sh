wantednode="lxplus427.cern.ch"
actualnode=`hostname`
if [ "x$actualnode" = "x$wantednode" ]
  then
  echo "Re-starting daemons on $wantednode"
  export DAEMONDIR=/afs/cern.ch/user/l/l1ccalib/testarea/17.2.0.2/Trigger/TrigT1/TrigT1CaloCAF/Daemons
  source $DAEMONDIR/setup.sh
  CORAL_AUTH_PATH=/afs/cern.ch/atlas/software/builds/AtlasCore/17.2.0/InstallArea/XML/AtlasAuthentication:$CORAL_AUTH_PATH
  CORAL_DBLOOKUP_PATH=/afs/cern.ch/atlas/software/builds/AtlasCore/17.2.0/InstallArea/XML/AtlasAuthentication:$CORAL_DBLOOKUP_PATH

  cd $DAEMONDIR/RunsProvider
  $DAEMONDIR/RunsProvider/RunsProviderDaemon.py restart

  cd $DAEMONDIR/JobOrganizer
  $DAEMONDIR/JobOrganizer/JobOrganizerDaemon.py restart

  cd $DAEMONDIR/W0Monitor
  $DAEMONDIR/W0Monitor/W0MonitorDaemon.py restart
else
  echo "Please use $wantednode"
fi
