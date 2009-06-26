source /afs/cern.ch/user/l/l1ccalib/Daemons/setup.sh

cd /afs/cern.ch/user/l/l1ccalib/Daemons/RunsProvider
/afs/cern.ch/user/l/l1ccalib/Daemons/RunsProvider/RunsProviderDaemon.py restart

cd /afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer
/afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer/JobOrganizerDaemon.py restart

cd /afs/cern.ch/user/l/l1ccalib/Daemons/W0Monitor
/afs/cern.ch/user/l/l1ccalib/Daemons/W0Monitor/W0MonitorDaemon.py restart
