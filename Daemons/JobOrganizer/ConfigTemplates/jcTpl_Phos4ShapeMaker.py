DaemonScriptsDir  = "#DAEMON_SCRIPTS_DIR#"
DaemonBackEndsDir = "#DAEMON_BACKENDS_DIR#"

JobWorkingDir  = "#JOB_WORKING_DIR#"
JobLogDir      = "#JOB_LOG_DIR#"
JobRootDir     = "#JOB_ROOT_DIR#"
JobPoolDir     = ""
JobConfigDir   = "#JOB_CONFIG_DIR#"
JobPostDir     =  "#JOB_POST_DIR#"

JobCastorDir="#CASTOR_DATA_DIR#/elecCalib/reconstruction"

AtlasRelease  = "15.6.9"

InputStageSVCClass = "atlcal"
OutputStageSVCClass = "atlcal"

BackEnd="CERN"
BatchQueue="atlasb1"
BatchGroup="u_ATLASLARCAL"
#BatchQueue="atlaslarcal"

JobScript = "submit.py"
AthenaLauncher = "athena_launcher_testarea.sh"

#jo template
JobOptionTemplate = "#DAEMON_JO_TEMPLATE_DIR#/Phos4ShapeMaker.tpl"

#jo name
JobOptionName = "#RUN_NUMBER#_#JOB_CONFIGURATION#_jobOptions.py"

#Athena log file
AthenaJobLogFile = JobOptionName.strip("_jobOptions.py")+'Athena.log'

RawDataFileBasePaths = ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED_8#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]

LogLevel = 2

OutputFiles = {
    "pprPhos4FullDelayData.txt": [(JobRootDir, "pprPhos4FullDelayData.txt")],
    "pprPhos4ProcessedSignalShapes.ps": [(JobRootDir, "pprPhos4ProcessedSignalShapes.ps")],
    "pprPhos4RawSignalShapes.ps": [(JobRootDir, "pprPhos4RawSignalShapes.ps")],
    "pprPhos4SignalShapes.root": [(JobRootDir, "pprPhos4SignalShapes.root")],
    AthenaJobLogFile:[(JobLogDir, AthenaJobLogFile)]
    }

JobPostTreatments = {
    "ALL":  ["#DAEMON_SCRIPTS_DIR#/ScanLogFiles.py"] }

#JobPostTreatments = [
#    {"ALL":   ["#DAEMON_SCRIPTS_DIR#/ScanLogFiles.py"]},
#    ]


#------------------------------------------------------------------------------------
# Mailing list
MailingList = ["veit.scharf@kip.uni-heidelberg.de"]
