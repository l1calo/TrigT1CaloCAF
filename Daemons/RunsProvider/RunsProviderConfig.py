dbConnection = "/afs/cern.ch/user/l/l1ccalib/testarea/15.2.0/Trigger/TrigT1/TrigT1CaloCAF/Daemons/db/rundb.db"

# MailingList = ["veit.scharf@kip.uni-heidelberg.de"]
#MailingList = ["prieur@cern.ch", "martin.wessels@cern.ch", "john.morris@cern.ch", "veit.scharf@kip.uni-heidelberg.de", "murrough.landon@cern.ch", "jb@hep.ph.bham.ac.uk", "pjwf@hep.ph.bham.ac.uk"]
MailingList = ["martin.wessels@cern.ch", "murrough.landon@cern.ch", "Bruce.Barnett@cern.ch", "jb@hep.ph.bham.ac.uk", "pjwf@hep.ph.bham.ac.uk"]

RawDataFileBasePaths = ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]

runListeners = {

                # Listener for LAr EnergyScan
                "LArEnergyScan": {
                    "tdaqdbname":"COOLONL_TDAQ/COMP200",
                    "trigdbname":"COOLONL_TRIGGER/COMP200",
                    "statusdbname":"COOLOFL_GLOBAL/COMP200",

                    "loglevel":0,
                    "oracle":False,
                    "reconly":True,
                    "detmask":0,
                    "runtype":"LarCalibL1Calo",
                    "tag":"",
                    "detstatus":"",
                    "detstatustag":"HEAD",
                    "daqpartition":["L1CaloCombined", "LArgL1CaloCombined"],
                    "tierzerotag":["L1CaloEnergyScan"],
                    "NOTtierzerotag":[],
                    "gainstrategy":[],

                    "format":"acertd",
                    "reverse":False,

                    "stoptimestamp":True,
                    "cleanstop":True,
                    "hasevents":False,
                    "minevents":1700,

                    #"initialrun":152000,
                    "initialrun":190000,

                    "fileslocations":["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
                },

                # Listener for Tile EnergyScan
                "TileEnergyScan": {
                    "tdaqdbname":"COOLONL_TDAQ/COMP200",
                    "trigdbname":"COOLONL_TRIGGER/COMP200",
                    "statusdbname":"COOLOFL_GLOBAL/COMP200",

                    "loglevel":0,
                    "oracle":False,
                    "reconly":True,
                    "detmask":0,
                    "runtype":"cismono",
                    "tag":"",
                    "detstatus":"2",
                    "detstatustag":"HEAD",
                    "daqpartition":["L1CaloCombined", "TileL1CaloCombined"],
                    "tierzerotag":["L1CaloEnergyScan"],
                    "NOTtierzerotag":[],
                    "gainstrategy":[],

                    "format":"acertd",
                    "reverse":False,

                    "stoptimestamp":True,
                    "cleanstop":True,
                    "hasevents":True,
                    "minevents":1700,

                    #"initialrun":152000,
                    "initialrun":190000,

                    "fileslocations": ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
                },

                # Listener for LAr EnergyScan HV
                "LArEnergyScanHV": {
                    "tdaqdbname":"COOLONL_TDAQ/COMP200",
                    "trigdbname":"COOLONL_TRIGGER/COMP200",
                    "statusdbname":"COOLOFL_GLOBAL/COMP200",

                    "loglevel":0,
                    "oracle":False,
                    "reconly":True,
                    "detmask":0,
                    "runtype":"LarCalibL1Calo",
                    "tag":"",
                    "detstatus":"",
                    "detstatustag":"HEAD",
                    "daqpartition":["L1CaloCombined", "LArgL1CaloCombined"],
                    "tierzerotag":["L1CaloEnergyScan"],
                    "NOTtierzerotag":[],
                    "gainstrategy":["CalibGainsEt"],

                    "format":"acertd",
                    "reverse":False,

                    "stoptimestamp":True,
                    "cleanstop":True,
                    "hasevents":False,
                    "minevents":1700,

                    #"initialrun":152000,
                    "initialrun":190000,

                    "fileslocations":["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
                },

                # Listener for Phos4Scan
                "L1CaloPhos4Scan": {
                    "tdaqdbname":"COOLONL_TDAQ/COMP200",
                    "trigdbname":"COOLONL_TRIGGER/COMP200",
                    "statusdbname":"COOLOFL_GLOBAL/COMP200",

                    "loglevel":0,
                    "oracle":False,
                    "reconly":True,
                    "detmask":0,
                    "runtype":"",
                    "tag":"",
                    "detstatus":"2",
                    "detstatustag":"HEAD",
                    "daqpartition":["L1CaloCombined", "LArgL1CaloCombined", "TileL1CaloCombined"],
                    "tierzerotag":["L1CaloPprPhos4ScanPars"],
                    "NOTtierzerotag":[],
                    "gainstrategy":[],

                    "format":"acertd",
                    "reverse":False,

                    "stoptimestamp":True,
                    "cleanstop":True,
                    "hasevents":True,
                    "minevents":0,

                    #"initialrun":152000,
                    "initialrun":190000,

                    "fileslocations": ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
                },

                # Listener for LAr Pulser run - LAr Master
                "LArCalibL1Calo": {
                    "tdaqdbname":"COOLONL_TDAQ/COMP200",
                    "trigdbname":"COOLONL_TRIGGER/COMP200",
                    "statusdbname":"COOLOFL_GLOBAL/COMP200",

                    "loglevel":0,
                    "oracle":False,
                    "reconly":True,
                    "detmask":0,
                    "runtype":"LarCalibL1Calo",
                    "tag":"",
                    "detstatus":"",
                    "detstatustag":"HEAD",
                    #"daqpartition":"",
                    #"daqpartition":["LArgL1Calo-TTC2LAN"],
                    "daqpartition":["L1CaloCombined", "LArgL1CaloCombined"],
                    "tierzerotag":[],
                    "NOTtierzerotag":["L1CaloEnergyScan", "L1CaloPprPhos4ScanPars"],
                    "gainstrategy":[],

                    "format":"acertd",
                    "reverse":False,

                    "stoptimestamp":True,
                    "cleanstop":True,
                    "hasevents":False,
                    "minevents":0,

                    #"initialrun":152000,
                    "initialrun":190000,

                    "fileslocations":["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
                },

                # Listener for Tile Pulser run - L1Calo Master
                "TileCalibL1Calo": {
                    "tdaqdbname":"COOLONL_TDAQ/COMP200",
                    "trigdbname":"COOLONL_TRIGGER/COMP200",
                    "statusdbname":"COOLOFL_GLOBAL/COMP200",

                    "loglevel":0,
                    "oracle":False,
                    "reconly":True,
                    "detmask":0,
                    "runtype":"cismono",
                    "tag":"",
                    "detstatus":"2",
                    "detstatustag":"HEAD",
                    #"daqpartition":["L1Calo-TTC2LAN",  "Tile-TTC2LAN", "TileL1Calo-TTC2LAN"],
                    "daqpartition":["L1CaloCombined", "TileL1CaloCombined"],
                    "tierzerotag":[],
                    "NOTtierzerotag":["L1CaloEnergyScan", "L1CaloPprPhos4ScanPars"],
                    "gainstrategy":[],

                    "format":"acertd",
                    "reverse":False,

                    "stoptimestamp":True,
                    "cleanstop":True,
                    "hasevents":True,
                    "minevents":0,

                    #"initialrun":152000,
                    "initialrun":190000,

                    "fileslocations": ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
                },

                # Listener for Standalone L1Calo runs
                "L1CaloStandalone": {
                    "tdaqdbname":"COOLONL_TDAQ/COMP200",
                    "trigdbname":"COOLONL_TRIGGER/COMP200",
                    "statusdbname":"COOLOFL_GLOBAL/COMP200",

                    "loglevel":0,
                    "oracle":False,
                    "reconly":True,
                    "detmask":0,
                    "runtype":"Physics",
                    "tag":"",
                    "detstatus":"2",
                    "detstatustag":"HEAD",
                    "daqpartition":["L1CaloStandalone", "L1CaloCalibration"],
                    "tierzerotag":[],
                    "NOTtierzerotag":[],
                    "gainstrategy":[],

                    "format":"acertd",
                    "reverse":False,

                    "stoptimestamp":True,
                    "cleanstop":True,
                    "hasevents":True,
                    "minevents":0,

                    #"initialrun":152000,
                    "initialrun":190000,

                    "fileslocations":["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
                }
}
