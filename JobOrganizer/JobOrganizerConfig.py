import os

dbconnection ="/afs/cern.ch/user/l/l1ccalib/Daemons/db/rundb.db"

DaemonInstallDir = os.environ["PWD"]

DaemonDataDir = os.environ["HOME"]+'/w0/DaemonData'

ConfigTemplateDir = DaemonInstallDir + '/ConfigTemplates'
JobOptionsTemplateDir = DaemonInstallDir + '/JobOptionsTemplates'
ScriptsDir = DaemonInstallDir + '/Scripts'
BackEndsDir = DaemonInstallDir + '/BackEnds'
DaemonLogDir = DaemonInstallDir + '/logs'

TmpDataDir = DaemonDataDir + '/tmp'
TmpInstallDir = DaemonInstallDir + '/tmp'

JobsWorkingDir = DaemonDataDir + '/jobs'

#CastorDataDir = "/castor/cern.ch/user/l/l1ccalib/w0/data"
#CastorDataDir = "/castor/cern.ch/user/p/prieur/w0/data"

# make sure that the stager is set to 'atlcal' !!!
CastorDataDir = "/castor/cern.ch/grid/atlas/caf/atlcal/perm/l1calo"



jobConfigurations = { "CBNT": {
								"listeners":             ["LArCalibL1Calo", "TileCalibL1Calo", ],
								"configurationTemplate": "jcTpl_CBNT_FastCalo.py",
								"validateJob":           False
							 },
		     "L1CaloStandalone": {
								"listeners":             ["L1CaloStandalone", ],
								"configurationTemplate": "jcTpl_CBNT_L1CaloOnly.py",
								"validateJob":           True
							 },

#		     "L1CaloStdAloneCBNT": {
#								"listeners":             ["L1CaloStandalone", ],
#								"configurationTemplate": "jcTpl_CBNT_L1CaloOnly.py",
#								"validateJob":           True
#							 },

#					   "LArRamp": {
#								"listeners":             ["LArCalibL1Calo"],
#								"configurationTemplate": "jobConfigurationTpl.py",
#								"validateJob":           True
#							 }
					}

atlaslarcalWatcher=	{"queue":"atlaslarcal",
					"account":"l1ccalib",
					"joblimit":15,
					"ncpu":44
					}

noWatcher=	{"queue":"8nm",
					"account":"l1ccalib",
					"joblimit":15,
					"ncpu":0
					}

ResourceWatcher = atlaslarcalWatcher

