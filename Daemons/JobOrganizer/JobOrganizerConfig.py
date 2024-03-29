import os

dbconnection ="/afs/cern.ch/user/l/l1ccalib/testarea/17.2.0.2/Trigger/TrigT1/TrigT1CaloCAF/Daemons/db/rundb.db"

DaemonInstallDir = os.environ["PWD"]
DaemonDataDir = os.environ["HOME"]+'/w0/DaemonData'
#DaemonDataDir = os.environ["HOME"]+'/w0/DaemonDataTest'
ConfigTemplateDir = DaemonInstallDir + '/ConfigTemplates'
JobOptionsTemplateDir = DaemonInstallDir + '/JobOptionsTemplates'
ScriptsDir = DaemonInstallDir + '/Scripts'
BackEndsDir = DaemonInstallDir + '/BackEnds'
DaemonLogDir = DaemonInstallDir + '/logs'
TmpDataDir = DaemonDataDir + '/tmp'
#TmpInstallDir = DaemonInstallDir + '/tmp'
TmpInstallDir = TmpDataDir
JobsWorkingDir = DaemonDataDir + '/jobs'
# make sure that the stager is set to 'atlcal' !!!
CastorDataDir = "/castor/cern.ch/grid/atlas/caf/atlcal/perm/l1calo"

jobConfigurations = { 
    #"CBNT_Release15": {
    #    "listeners":             ["LArCalibL1Calo", "TileCalibL1Calo", "LArEnergyScan", "TileEnergyScan", "L1CaloPhos4Scan"],
    #    "configurationTemplate": "jcTpl_CBNT_Release15_FastCalo.py",
    #    "validateJob":           False
    #    },
    #"L1CaloStandalone": {
    #    "listeners":             ["L1CaloStandalone"],
    #    "configurationTemplate": "jcTpl_CBNT_L1CaloOnly.py",
    #    "validateJob":           True
    #    },
    #"L1CaloStandalone_Release15": {
    #    "listeners":             ["L1CaloStandalone"],
    #    "configurationTemplate": "jcTpl_CBNT_Release15_L1CaloOnly.py",
    #    "validateJob":           True
    #    },
    "LArL1CaloRampMaker" : {
        "listeners":             ["LArEnergyScan", "LArEnergyScanHV"],
        "configurationTemplate": "jcTpl_LArL1CaloRampMaker.py",
        "validateJob":           False
        },
    #"LArL1CaloRampMaker_FCAL" : {
    #    "listeners":             ["LArEnergyScan"],
    #    "configurationTemplate": "jcTpl_LArL1CaloRampMaker_FCAL.py",
    #    "validateJob":           False
    #},
    "TileL1CaloRampMaker" : {
        "listeners":             ["TileEnergyScan"],
        "configurationTemplate": "jcTpl_TileL1CaloRampMaker.py",
        "validateJob":           False
        },
    "LArL1CaloHV" : {
        "listeners":             ["LArEnergyScanHV"],
        "configurationTemplate": "jcTpl_LArL1CaloHV.py",
        "validateJob":           False
        },
    "Phos4ShapeMaker" : {
        "listeners":             ["L1CaloPhos4Scan"],
        "configurationTemplate": "jcTpl_Phos4ShapeMaker.py",
        "validateJob":           False
        },
    "L1CaloCalibD3PD" : {
        "listeners":             ["LArCalibL1Calo", "TileCalibL1Calo", "LArEnergyScan", "TileEnergyScan", "L1CaloPhos4Scan", "L1CaloStandalone"],
        "configurationTemplate": "jcTpl_L1CaloCalibD3PD.py",
        "validateJob":           True
        }
    }

atlaslarcalWatcher = {
    #"queue":"atlaslarcal",
    "queue":"atlasb1",
    "account":"l1ccalib",
    "group":"u_ATLASLARCAL",
    "joblimit":15,
    "ncpu":44
    }

noWatcher = {
    "queue": "8nm",
    "account": "l1ccalib",
    "joblimit": 15,
    "ncpu": 0
    }

ResourceWatcher = atlaslarcalWatcher

