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

#AtlasRelease  = "15.6.9"
#AtlasRelease  = "16.6.7.3"
AtlasRelease  = "17.0.3.4"

InputStageSVCClass = "atlcal"
OutputStageSVCClass = "atlcal"

BackEnd="CERN"
BatchQueue="atlasb1"
BatchGroup="u_ATLASLARCAL"
#BatchQueue="atlaslarcal"

JobScript = "submit.py"
AthenaLauncher = "athena_launcher_testarea.sh"

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
    "L1CaloRampData.pool.root": [(JobRootDir, "L1CaloRampData.pool.root")],
    "PoolFileCatalog.xml": [(JobRootDir, "PoolFileCatalog.xml")],
    "energyscanresults.sqlite": [(JobRootDir, "energyscanresults.sqlite")],
    "rampdata.xml": [(JobRootDir, "rampdata.xml")],
    "graphs.root": [(JobRootDir, "graphs.root")],
    "bad-ofciter.txt": [(JobRootDir, "bad-ofciter.txt")],
    "bad_gains.txt": [(JobRootDir, "bad_gains.txt")],
    "drifted_towers.txt": [(JobRootDir, "drifted_towers.txt")],
    "Gains.ps":  [(JobRootDir, "Gains_#RUN_NUMBER#.ps")],
    "Gains.pdf":  [(JobRootDir, "Gains_#RUN_NUMBER#.pdf")],
    "rampPlots.ps":  [(JobRootDir, "rampPlots_#RUN_NUMBER#.ps")],
    "rampPlots.pdf":  [(JobRootDir, "rampPlots_#RUN_NUMBER#.pdf")],
    AthenaJobLogFile:[(JobLogDir, AthenaJobLogFile)]
    }

#JobPostTreatments = [
#    {"DONE":  ["#DAEMON_SCRIPTS_DIR#/PlotCalibrationGains.py"],
#     "ALL":   ["#DAEMON_SCRIPTS_DIR#/ScanLogFiles.py"]},
#    ]
JobPostTreatments = {
    "DONE": ["#DAEMON_SCRIPTS_DIR#/PlotCalibrationGains.sh"],
    "ALL":  ["#DAEMON_SCRIPTS_DIR#/ScanLogFiles.py"] }


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
#MailingList = ["veit.scharf@kip.uni-heidelberg.de"]
MailingList = ["pjwf@hep.ph.bham.ac.uk"]
