dbConnection = "/afs/cern.ch/user/l/l1ccalib/testarea/15.2.0/Trigger/TrigT1/TrigT1CaloCAF/Daemons/db/rundb.db"

MailingList = ["prieur@cern.ch"]

RawDataFileBasePaths = ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]

runListeners = {

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

                    "format":"acertd",
                    "reverse":False,

                    "stoptimestamp":True,
                    "cleanstop":True,
                    "hasevents":False,

                    "initialrun":113232,

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

                   "format":"acertd",
                   "reverse":False,

                   "stoptimestamp":True,
                   "cleanstop":True,
                   "hasevents":True,

                   "initialrun":104000,

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
                    "daqpartition":["L1CaloStandalone"],

                    "format":"acertd",
                    "reverse":False,

                    "stoptimestamp":True,
                    "cleanstop":True,
                    "hasevents":True,

                    "initialrun":113232,

                    "fileslocations":["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
                }
}
