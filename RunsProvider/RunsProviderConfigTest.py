dbConnection = "/afs/cern.ch/user/l/l1ccalib/Daemons/RunsProvider/rundbtest.db"

MailingList = ["prieur@cern.ch"]

RawDataFileBasePaths = ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]

runListeners = {

#				"LArCalibL1Calo": {
#					"tdaqdbname":"COOLONL_TDAQ/COMP200",
#					"trigdbname":"COOLONL_TRIGGER/COMP200",
#					"statusdbname":"COOLOFL_GLOBAL/COMP200",
#
#					"loglevel":0,
#					"oracle":False,
#					"reconly":True,
#					"detmask":0,
#					"runtype":"LarCalibL1Calo",
#					"tag":"",
#					"detstatus":"",
#					"detstatustag":"HEAD",
#					#"daqpartition":"",
#					"daqpartition":"LArgL1Calo-TTC2LAN",
#
#					"format":"acertd",
#					"reverse":False,
#
#					"stoptimestamp":True,
#					"cleanstop":True,
#					"hasevents":False,
#
#					"initialrun":113232,
#
#					"fileslocations":["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
#				},

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
					"daqpartition":"Tile-TTC2LAN",

					"format":"acertd",
					"reverse":False,

					"stoptimestamp":True,
					"cleanstop":True,
					"hasevents":True,

					"initialrun":113232,

					"fileslocations": ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
				},

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
					"daqpartition":"L1Calo-TTC2LAN",

					"format":"acertd",
					"reverse":False,

					"stoptimestamp":True,
					"cleanstop":True,
					"hasevents":True,

					"initialrun":113232,

					"fileslocations": ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
				},

#				"L1CaloStandalone": {
#					"tdaqdbname":"COOLONL_TDAQ/COMP200",
#					"trigdbname":"COOLONL_TRIGGER/COMP200",
#					"statusdbname":"COOLOFL_GLOBAL/COMP200",
#
#					"loglevel":0,
#					"oracle":False,
#					"reconly":True,
#					"detmask":0,
#					"runtype":"Physics",
#					"tag":"",
#					"detstatus":"2",
#					"detstatustag":"HEAD",
#					"daqpartition":"L1CaloStandalone",
#
#					"format":"acertd",
#					"reverse":False,
#
#					"stoptimestamp":True,
#					"cleanstop":True,
#					"hasevents":True,
#
#					"initialrun":113232,
#
#					"fileslocations":["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]
#				}
}
