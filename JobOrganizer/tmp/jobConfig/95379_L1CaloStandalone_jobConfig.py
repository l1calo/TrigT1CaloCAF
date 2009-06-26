
DaemonScriptsDir  = "/afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer/Scripts"
DaemonBackEndsDir = "/afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer/BackEnds"

JobWorkingDir = "/afs/cern.ch/user/l/l1ccalib/w0/DaemonData/jobs/95379_L1CaloStandalone"
JobLogDir     = "/afs/cern.ch/user/l/l1ccalib/w0/DaemonData/jobs/95379_L1CaloStandalone/log"
JobRootDir    = "/afs/cern.ch/user/l/l1ccalib/w0/DaemonData/jobs/95379_L1CaloStandalone/root"
#JobPoolDir    = "/afs/cern.ch/user/l/l1ccalib/w0/DaemonData/jobs/95379_L1CaloStandalone/pool"
JobPoolDir    = ""
JobConfigDir  = "/afs/cern.ch/user/l/l1ccalib/w0/DaemonData/jobs/95379_L1CaloStandalone/config"
JobPostDir    = "/afs/cern.ch/user/l/l1ccalib/w0/DaemonData/jobs/95379_L1CaloStandalone/post"

#JobCastorDir="#JOB_CASTOR_DIR#"
JobCastorDir="/castor/cern.ch/grid/atlas/caf/atlcal/perm/l1calo/elecCalib/reconstruction"

AtlasRelease  = "14.2.23.2"

InputStageSVCClass = "t0atlas"
OutputStageSVCClass = "atlcal"

BackEnd="CERN"
BatchQueue="atlaslarcal"
#BatchQueue="8nm"

JobScript = "submit.py"
AthenaLauncher = "athena_launcher.sh"

#jo template
JobOptionTemplate = "/afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer/JobOptionsTemplates/RecExCommission_L1CaloOnly.tpl"

#jo name
JobOptionName    = "95379_L1CaloStandalone_jobOptions.py"

#Athena log file
AthenaJobLogFile = JobOptionName.strip("_jobOptions.py")+'Athena.log'

RawDataFileBasePaths = ["/castor/cern.ch/grid/atlas/DAQ/l1calo/00095379","/castor/cern.ch/grid/atlas/DAQ/l1calo/0095379", "/castor/cern.ch/grid/atlas/DAQ/l1calo/95379", "/castor/cern.ch/grid/atlas/DAQ/l1calo"]

LogLevel = 2

#AdditionalInputFiles = [("/afs/cern.ch/user/l/l1ccalib/w0/DaemonData/jobs/95379_L1CaloStandalone/config/",""),("/afs/cern.ch/user/l/l1ccalib/w0/DaemonData/jobs/95379_L1CaloStandalone/config/","config")]

#OutputFilesPath={"CBNT":JobRootDir, "POOL":JobPoolDir, "LOG":JobLogDir}
#OutputFiles = [ "cosmics.ntuple", "sdfsdf"]
OutputFiles = { "cosmics.ntuple.root":[(JobRootDir, "95379_L1CaloStandalone.ntuple.root")],
				AthenaJobLogFile:[(JobLogDir, AthenaJobLogFile)]
			  }



#JobPostTreatments = {"DONE":   ["/afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer/Scripts/ScanLogFiles.py"],
#                     "ABORTED":["/afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer/Scripts/ScanLogFiles.py]"}

JobPostTreatments = [ {"ALL":   ["/afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer/Scripts/ScanLogFiles.py"]},
					]


#JobPostTreatments = [{"ALL":[,]},
#					  {"DONE":   ["/afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer/Scripts/ScanLogFiles.py"], "ABORTED":["/afs/cern.ch/user/l/l1ccalib/Daemons/JobOrganizer/Scripts/ScanLogFiles.py]"},
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

MailingList=["prieur@cern.ch"]
