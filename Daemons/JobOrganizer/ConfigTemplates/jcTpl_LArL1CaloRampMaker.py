DaemonScriptsDir  = "#DAEMON_SCRIPTS_DIR#"
DaemonBackEndsDir = "#DAEMON_BACKENDS_DIR#"

JobWorkingDir  = "#JOB_WORKING_DIR#"
JobLogDir      = "#JOB_LOG_DIR#"
JobRootDir     = "#JOB_ROOT_DIR#"
JobTestAreaDir = JobRootDir + "/testarea"
JobPoolDir     = ""
JobConfigDir   = "#JOB_CONFIG_DIR#"
JobPostDir     = "#JOB_POST_DIR#"

JobCastorDir="#CASTOR_DATA_DIR#/elecCalib/reconstruction"

AtlasRelease  = "15.5.1.6"

InputStageSVCClass = "atlcal"
OutputStageSVCClass = "atlcal"

BackEnd="CERN"
BatchQueue="atlaslarcal"

JobScript = "submit_and_checkout.py"
AthenaLauncher = "athena_launcher_checkout.sh"
Packages = ["Trigger/TrigT1/TrigT1CaloCalibConditions",
            "Trigger/TrigT1/TrigT1CaloCalibAthenaPool",
            "Trigger/TrigT1/TrigT1CaloCalibTools",
            "Trigger/TrigT1/TrigT1CaloCalibUtils"]

#jo template
JobOptionTemplate = "#DAEMON_JO_TEMPLATE_DIR#/LArL1CaloRampMaker.tpl"

#jo name
JobOptionName = "#RUN_NUMBER#_#JOB_CONFIGURATION#_jobOptions.py"

#Athena log file
AthenaJobLogFile = JobOptionName.strip("_jobOptions.py")+'Athena.log'

RawDataFileBasePaths = ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED_8#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]

LogLevel = 2

#OutputFilesPath={"CBNT":JobRootDir, "POOL":JobPoolDir, "LOG":JobLogDir}
OutputFiles = {
    "testarea/L1CaloRampData.pool.root": [(JobRootDir, "L1CaloRampData.pool.root")],
    "testarea/PoolFileCatalog.xml": [(JobRootDir, "PoolFileCatalog.xml")],
    "testarea/energyscanresults.sqlite": [(JobRootDir, "energyscanresults.sqlite")],
    "testarea/rampdata.xml": [(JobRootDir, "rampdata.xml")],
    "testarea/graphs.root": [(JobRootDir, "graphs.root")],
    "testarea/" + AthenaJobLogFile:[(JobLogDir, AthenaJobLogFile)]
    }

JobPostTreatments = [
    {"ALL":   ["#DAEMON_SCRIPTS_DIR#/ScanLogFiles.py"]},
    ]


#JobPostTreatments = [{"ALL":[,]},
#					  {"DONE":   ["#DAEMON_SCRIPTS_DIR#/ScanLogFiles.py"], "ABORTED":["#DAEMON_SCRIPTS_DIR#/ScanLogFiles.py]"},
#					  {"ALL":[,]}
#					  ]

#CastorBackupArea = ""


# For each job type, define :
#      topJobOption  : name of the topJobOption file ( TopJobOptionDirectory will be preprend )
#      jobOptionName : syntax of the jobOption file name  ( same syntax will be used for every file related with job submission )
#      backend       : job submission backend   ( the backend parameters are defined below )

#JobSubmission_Job_PostTreatment={"DONE":"ScanLogFiles.py","FAILED":"ScanLogFiles.py"}
#JobSubmission_Final_PostTreatment={"ALL":"MergeSQLiteFiles.py"}

#JobSubmission_Automatic_Archive_PostTreatment=1
#JobSubmission_Archive_PostTreatment={"ALL":"ArchiveData.py"}

#------------------------------------------------------------------------------------
# Mailing list
MailingList = ["veit.scharf@kip.uni-heidelberg.de"]