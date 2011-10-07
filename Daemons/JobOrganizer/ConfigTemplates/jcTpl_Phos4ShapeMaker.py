DaemonScriptsDir  = "#DAEMON_SCRIPTS_DIR#"
DaemonBackEndsDir = "#DAEMON_BACKENDS_DIR#"

JobWorkingDir  = "#JOB_WORKING_DIR#"
JobLogDir      = "#JOB_LOG_DIR#"
JobRootDir     = "#JOB_ROOT_DIR#"
JobPoolDir     = ""
JobConfigDir   = "#JOB_CONFIG_DIR#"
JobPostDir     =  "#JOB_POST_DIR#"

JobCastorDir="#CASTOR_DATA_DIR#/elecCalib/reconstruction"

#AtlasRelease  = "15.6.9"
#AtlasRelease  = "16.0.3.3"
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
JobOptionTemplate = "#DAEMON_JO_TEMPLATE_DIR#/Phos4ShapeMaker.tpl"

#jo name
JobOptionName = "#RUN_NUMBER#_#JOB_CONFIGURATION#_jobOptions.py"

#Athena log file
AthenaJobLogFile = JobOptionName.strip("_jobOptions.py")+'Athena.log'

RawDataFileBasePaths = ["/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED_8#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER_PADDED#", "/castor/cern.ch/grid/atlas/DAQ/l1calo/#RUN_NUMBER#", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]

LogLevel = 2

OutputFiles = {
    "rawMax_#RUN_NUMBER_PADDED_8#.txt": [(JobRootDir, "rawMax_#RUN_NUMBER_PADDED_8#.txt")],
    "rawFit_#RUN_NUMBER_PADDED_8#.txt": [(JobRootDir, "rawFit_#RUN_NUMBER_PADDED_8#.txt")],
    "processedMax_#RUN_NUMBER_PADDED_8#.txt": [(JobRootDir, "processedMax_#RUN_NUMBER_PADDED_8#.txt")],
    "processedFit_#RUN_NUMBER_PADDED_8#.txt": [(JobRootDir, "processedFit_#RUN_NUMBER_PADDED_8#.txt")],
    "rawShapes_#RUN_NUMBER_PADDED_8#.ps.gz": [(JobRootDir, "rawShapes_#RUN_NUMBER_PADDED_8#.ps.gz")],
    "processedShapes_#RUN_NUMBER_PADDED_8#.ps.gz": [(JobRootDir, "processedShapes_#RUN_NUMBER_PADDED_8#.ps.gz")],
    "shapeMakerData_#RUN_NUMBER_PADDED_8#.root": [(JobRootDir, "shapeMakerData_#RUN_NUMBER_PADDED_8#.root")],
    "summary_#RUN_NUMBER_PADDED_8#.ps.gz": [(JobRootDir, "summary_#RUN_NUMBER_PADDED_8#.ps.gz")],
    "summary_#RUN_NUMBER_PADDED_8#.pdf": [(JobRootDir, "summary_#RUN_NUMBER_PADDED_8#.pdf")],
    "summary_#RUN_NUMBER_PADDED_8#.root": [(JobRootDir, "summary_#RUN_NUMBER_PADDED_8#.root")],
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
