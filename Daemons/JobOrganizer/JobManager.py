#!/usr/bin/env python

import os, sys, logging, commands, time
import stat
from datetime import datetime
from datetime import timedelta
from ResourceWatcher import *
import Tools


class Stager:
	def __init__(self, stager=""):
		self.stager = stager
		return


	def stage(self, fileList, stager_get=True):

		old_stager =  os.environ["STAGE_SVCCLASS"]
		# changer stager
		if self.stager!="":
			#cmd = "export STAGE_SVCCLASS="+self.stager
			#rawOutput = commands.getoutput(cmd)
			os.environ["STAGE_SVCCLASS"]=self.stager


		statusDict= {'NOTSTAGED':0, 'STAGEIN':1, 'STAGED':2}
		globalStatus = 'STAGED'

		for dataFile in fileList:

			# not a castor file, skip to next file
			if dataFile.find('/castor/')==-1:
				continue

			sStatus = self.fileStatus(dataFile)
			if sStatus!='STAGED':
				if sStatus=='NOTSTAGED':

					if statusDict[sStatus]<statusDict[globalStatus]: globalStatus = 'NOTSTAGED'

					# file not staged
					if stager_get:
						cmd =  "stager_get -M "+ dataFile
						rawOutput = commands.getoutput(cmd)
						#print rawOutput

				elif sStatus=='STAGEIN':
					if statusDict[sStatus]<statusDict[globalStatus]: globalStatus = 'STAGEIN'

				else:
					globalStatus = 'STAGEUDF'
					print 'something went wrong'


		if self.stager!="":
			#cmd = "export STAGE_SVCCLASS="+old_stager
			#rawOutput = commands.getoutput(cmd)
			os.environ["STAGE_SVCCLASS"]=old_stager

		return str(globalStatus)


	def fileStatus(self, path):

		old_stager =  os.environ["STAGE_SVCCLASS"]
		# changer stager
		if self.stager!="":
			#cmd = "export STAGE_SVCCLASS="+self.stager
			#rawOutput = commands.getoutput(cmd)
			os.environ["STAGE_SVCCLASS"]=self.stager

		# get gile information
		cmd =  "stager_qry -M "+ path
		rawOutput = commands.getoutput(cmd).splitlines()[1]
		#print rawOutput

		output = ""
		if rawOutput.find("STAGED")!=-1 or rawOutput.find("CANBEMIGR")!=-1:
			output= 'STAGED'

		elif rawOutput.find("Error 2")!=-1:
			output= 'NOTSTAGED'

		elif rawOutput.find("STAGEIN")!=-1:
			output= 'STAGEIN'

		else:
			output= 'STAGEUDF'

		if self.stager!="":
			#cmd = "export STAGE_SVCCLASS="+self.stager
			#rawOutput = commands.getoutput(cmd)
			os.environ["STAGE_SVCCLASS"]=old_stager

		return output


class Job:

	def __init__(self, jobInformation):

		self.jobInformation = jobInformation

		self.workingAreaStatus = False
		self.isSubmitted = False
		self.isPrepared=False

		self.inputRawDataFiles = []

		self.resourceWatcher = None

		self.createFolderStructure()
		self.initLogging(self.name())

		self.datefmt='%Y-%m-%d %H:%M'


		return

	def initLogging(self, name):
		#create logger
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.DEBUG)
		self.logger.setLevel(self.jobInformation.jobConfigModule.LogLevel)

		#create file handler and set level to debug
		logFile = self.jobInformation.jobConfigModule.JobLogDir+'/Job_'+self.jobInformation.runNumber+'_'+self.jobInformation.jobConfiguration.name+'.log'
		#fh = logging.FileHandler(logFile,'w')
		fh = logging.FileHandler(logFile)
		#fh.setLevel(logging.DEBUG)
		fh.setLevel(self.jobInformation.jobConfigModule.LogLevel)

		#create formatter
		formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s", datefmt='%Y-%m-%d %H:%M')

		#add formatter to fh
		fh.setFormatter(formatter)

		#add ch to logger
		self.logger.addHandler(fh)

	def name(self):
		return self.jobInformation.runNumber+"_"+self.jobInformation.jobConfiguration.name

	def status(self):
		if self.jobInformation!=None:
			return self.jobInformation.status

	def prepareForSubmission(self):
		self.logger.debug("from prepareForSubmission()")
		if self.isPrepared:
			self.logger.debug("job already 'prepared'")
			return

		if not self.workingAreaStatus and self.jobInformation.status != 'ABORTED':
			self.logger.debug("preparing working area")
			bStatus = True
			# find data files
			bStatus &= self.findRawDataFiles()
			if not bStatus: self.logger.warning("FindRawDataFiles failed.")
			self.logger.debug(self.inputRawDataFiles)

			# prepare area and copy files
			bStatus &= self.setupWorkingArea()
			if not bStatus: self.logger.warning("SetupWorkingArea failed.")

			if bStatus:
				self.logger.debug("work area prepared")
				self.workingAreaStatus = True #if everthing is fine
			else:
				self.logger.warning("Something went wrong when setting up the work area")
				self.logger.warning("new job status: ABORTED")
				self.jobInformation.setStatus("ABORTED")

		if self.workingAreaStatus:
			stageStatus = self.stageRawData()
			self.logger.debug("staging files - job status: "+stageStatus)
			self.jobInformation.setStatus(stageStatus)

		if self.workingAreaStatus and self.jobInformation.status=='STAGED':
			self.logger.debug("job is now prepared for running")
			self.isPrepared = True

		self.logger.debug("end of prepareForSubmission()")
		return


	def findRawDataFiles(self):
		for path in self.jobInformation.jobConfigModule.RawDataFileBasePaths:
			filesList = Tools.listFiles(path, self.jobInformation.runNumber)
			if filesList!=[]:
				self.inputRawDataFiles = filesList
				break
		return True


	def setupWorkingArea(self):
		bStatus = True

		#create folder if not already existing
		#bStatus &= self.createFolderStructure()

		#copy files
		bStatus &= self.copyFiles()

		return bStatus


	def createFolderStructure(self):
		bStatus = True
		bStatus &= Tools.createFolder(self.jobInformation.jobConfigModule.JobWorkingDir)
		bStatus &= Tools.createFolder(self.jobInformation.jobConfigModule.JobLogDir)
		bStatus &= Tools.createFolder(self.jobInformation.jobConfigModule.JobRootDir)
		bStatus &= Tools.createFolder(self.jobInformation.jobConfigModule.JobPoolDir)
		bStatus &= Tools.createFolder(self.jobInformation.jobConfigModule.JobConfigDir)
		bStatus &= Tools.createFolder(self.jobInformation.jobConfigModule.JobPostDir)
		return bStatus


	def copyFiles(self):
		self.logger.debug("copying files for working area")
		bStatus = True

		athenaSetupDir = self.jobInformation.jobConfigModule.DaemonBackEndsDir+'/'+self.jobInformation.jobConfigModule.BackEnd+'/'+self.jobInformation.jobConfigModule.AtlasRelease

		bStatus &= Tools.copyFile(athenaSetupDir+'/requirements', self.jobInformation.jobConfigModule.JobConfigDir)
		if not bStatus: self.logger.warning("Copying files from %s to %s failed." % (athenaSetupDir+'/requirements', self.jobInformation.jobConfigModule.JobConfigDir))

		# add a few tag required by localAthena_setup.sh
		atlasRelease = self.jobInformation.jobConfigModule.AtlasRelease
		atlasReleaseNoCache = str('.').join(atlasRelease.split(".")[0:3]) # removes the cache version

		self.jobInformation.placeHolders["#ATLAS_RELEASE#"]         = str(atlasRelease)
		self.jobInformation.placeHolders["#ATLAS_RELEASE_NOCACHE#"] = str(atlasReleaseNoCache)
		self.jobInformation.placeHolders["#INPUT_STAGE_SVC_CLASS#"]       = str(self.jobInformation.jobConfigModule.InputStageSVCClass)
		self.jobInformation.placeHolders["#OUTPUT_STAGE_SVC_CLASS#"]       = str(self.jobInformation.jobConfigModule.OutputStageSVCClass)
		self.jobInformation.placeHolders["#JOB_OPTIONS_NAME#"]       = str(self.jobInformation.jobConfigModule.JobOptionName)
		self.jobInformation.placeHolders["#JOB_LOG_NAME#"]       = str(self.jobInformation.jobConfigModule.AthenaJobLogFile)

		bStatus &= Tools.replaceTag(athenaSetupDir+'/'+self.jobInformation.jobConfigModule.AthenaLauncher, self.jobInformation.jobConfigModule.JobConfigDir, self.jobInformation.placeHolders)
		if not bStatus: self.logger.warning("Replacing tags for athena launcher %s to file %s with dictionary %s failed." %\
						    (athenaSetupDir+'/'+self.jobInformation.jobConfigModule.AthenaLauncher,\
						     self.jobInformation.jobConfigModule.JobConfigDir,\
						     self.jobInformation.placeHolders))

		#copy jobConfiguration
		bStatus &= Tools.copyFile(self.jobInformation.jobConfigModulePath, self.jobInformation.jobConfigModule.JobConfigDir)
		if not bStatus: self.logger.warning("Copying jobConfiguration from %s to %s failed." %\
						    (self.jobInformation.jobConfigModulePath, self.jobInformation.jobConfigModule.JobConfigDir))

		#copy jobOptions
		self.jobInformation.placeHolders["#RAW_DATA_SETS#"]=self.makeRAWDATASETS()
		bStatus &= Tools.replaceTag(self.jobInformation.jobConfigModule.JobOptionTemplate, self.jobInformation.jobConfigModule.JobConfigDir+'/'+self.jobInformation.jobConfigModule.JobOptionName, self.jobInformation.placeHolders)
		if not bStatus: self.logger.warning("Replacing tags for jobOptions file %s to file %s with dictionary %s failed." %\
						    (self.jobInformation.jobConfigModule.JobOptionTemplate,\
						     self.jobInformation.jobConfigModule.JobConfigDir+'/'+self.jobInformation.jobConfigModule.JobOptionName,\
						     self.jobInformation.placeHolders))
						    
		#copy scripts
		self.jobInformation.placeHolders["#JOB_CONFIGURATION_LOCAL#"]=self.jobInformation.jobConfigModule.JobConfigDir.rstrip('/')+'/'+os.path.split(self.jobInformation.jobConfigModulePath)[1]

		#replace tag submit script
		bStatus &= Tools.replaceTag(self.jobInformation.jobConfigModule.DaemonScriptsDir.rstrip('/')+'/'+self.jobInformation.jobConfigModule.JobScript, self.jobInformation.jobConfigModule.JobConfigDir, self.jobInformation.placeHolders)
		os.chmod(self.jobInformation.jobConfigModule.JobConfigDir+'/'+self.jobInformation.jobConfigModule.JobScript,stat.S_IRWXG |stat.S_IRWXO |stat.S_IRWXU )
		if not bStatus: self.logger.warning("Replacing tags for submit script %s to %s with %s failed." %\
						    (self.jobInformation.jobConfigModule.DaemonScriptsDir.rstrip('/')+'/'+self.jobInformation.jobConfigModule.JobScript,\
						     self.jobInformation.jobConfigModule.JobConfigDir,
						     self.jobInformation.placeHolders))

		#copy additionnal input files (like other sub-joboptions)
		#self.jobInformation.jobConfigModule.AdditionalInputFiles

		return bStatus


	def makeRAWDATASETS(self):
		print 'makeRAWDATASETS'
		output = []
		output.append('athenaCommonFlags.BSRDOInput = [\n')

		for rawFile in self.inputRawDataFiles:
			print 'tutu: ',rawFile
			output.append('"' + rawFile + '",\n')

		output.append(']\n')
		return ''.join(output)


	def prepared(self):
		return self.isPrepared


	def stageRawData(self):
		#get stage status
		return Stager(self.jobInformation.jobConfigModule.InputStageSVCClass).stage(self.inputRawDataFiles) #'STAGED' or 'STAGING' or 'NOTSTAGED' or 'STAGEUDF'


	def stageStatus(self):
		# we only retrieve the golbal status, stager_get is not called
		return Stager(self.jobInformation.jobConfigModule.InputStageSVCClass).stage(self.inputRawDataFiles, False) #'STAGED' or 'STAGING' or 'NOTSTAGED' or 'STAGEUDF'


	def updateStatus(self):
		self.logger.debug("from updateStatus()")

		if self.submitted():
			self.logger.debug("job already submitted - getting status from ressourceWatcher")

			#check time from submission
			#if <10s do nothing, it sometime gets several seconds before a run appear in bjobs command
			sdate = datetime.strptime(self.jobInformation.jobStart, self.datefmt)
			ndate = datetime.now() - timedelta(minutes=1)

			if sdate<ndate:
				#get info from ResourceWatcher
				print self.jobInformation.batchid
				batchJob = self.resourceWatcher.getJobById(self.jobInformation.batchid)
				self.logger.debug(str(batchJob))
				if batchJob==None or batchJob.state=='EXIT' or batchJob.state=='DONE':
					self.jobInformation.setStatus('DONE')
					self.jobInformation.setStopTime(time.strftime(self.datefmt))
					self.logger.debug("job no longer running - seting status to DONE")

				else:
					print batchJob.state
					self.logger.debug("job batch status: "+batchJob.state)
					self.jobInformation.setStatus(batchJob.state)

		elif self.prepared():
			self.logger.debug("job prepared - checking that files are still staged")
			#check that files are still staged
			stageStatus = self.stageStatus()
			if stageStatus!='STAGED':
				self.jobInformation.setStatus(stageStatus)
				self.isPrepared = False
				self.logger.debug("files are no longer staged - new status: "+stageStatus)

		else:
			print 'job not prepared'
			stageStatus = self.stageStatus()
			self.logger.debug("job not prepared - current status: "+stageStatus)
			#update staging information
			self.jobInformation.setStatus(stageStatus)

		self.logger.debug("end of updateStatus()")
		return


	def submitted(self):
		return self.isSubmitted


	def submit(self):
		self.logger.debug("from submit()")
		jobName = self.jobInformation.runNumber+'_'+self.jobInformation.jobConfiguration.name
		scriptName = self.jobInformation.jobConfigModule.JobConfigDir+'/'+self.jobInformation.jobConfigModule.JobScript

		print scriptName
		if self.jobInformation.jobConfigModule.BatchGroup=='':
		        cmd = 'bsub -q' + self.jobInformation.jobConfigModule.BatchQueue + ' -o ' + self.jobInformation.jobConfigModule.JobLogDir + '/' + jobName+'.out' + ' -J' + jobName + ' ' + scriptName 
		else:
		        cmd = 'bsub -q' + self.jobInformation.jobConfigModule.BatchQueue + ' -G ' + self.jobInformation.jobConfigModule.BatchGroup + ' -o ' + self.jobInformation.jobConfigModule.JobLogDir + '/' + jobName+'.out' + ' -J' + jobName + ' ' + scriptName
		rawOutput = commands.getoutput(cmd).splitlines()[0]
		self.logger.debug("submitting job:")
		self.logger.debug(cmd)
		self.logger.debug(rawOutput)

		#['atlaslarcal: User cannot use the queue. Job not submitted.']
		#['Job <15468385> is submitted to queue <8nm>.']

		if rawOutput.find('<')==-1:
			self.isSubmitted = False
			self.logger.debug("something went wrong when submitting the job - job not submitted")
			return

		self.jobInformation.setBatchId(rawOutput[rawOutput.find('<')+1:rawOutput.find('>')])
		print self.jobInformation.batchid
		self.isSubmitted = True

		self.jobInformation.setStartTime(time.strftime(self.datefmt))
		#time.strptime(time.strftime(datefmt),datefmt)

		self.logger.debug("end of submit()")
		return

	def checkProcessedOk(self):
		self.logger.debug("from checkProcessedOk()")

		#open log file
		path = self.jobInformation.jobConfigModule.JobLogDir+'/'+self.jobInformation.jobConfigModule.AthenaJobLogFile
		pOk = Tools.checkProcessedOk(path)

		if pOk:
			self.jobInformation.setResult("OK")
			self.logger.debug("OK")
		else:
			self.jobInformation.setResult("FAILED")
			self.logger.debug("FAILED")

		self.logger.debug("end of checkProcessedOk()")
		return pOk


	def postProcessing(self):

		#build a list of scripts to execute
		scriptList=[]
		postTreatmentsList = self.jobInformation.jobConfigModule.JobPostTreatments
		for postTreatmentsDict in postTreatmentsList:
			postTreatments = postTreatmentsDict[self.status()]
			if postTreatments==None:
				postTreatments = postTreatmentsDict['ALL']
			else:
				postTreatments.append(postTreatmentsDict['ALL'])

			for postTreatment in postTreatments:

				#copyFile(self.jobInformation.jobConfigModule.DaemonScriptsDir+'/'+script, self.jobInformation.jobConfigModule.JobPostDir)
				# probably have to use replaceTag

				localScript = self.jobInformation.jobConfigModule.JobPostDir+'/'+script
				scriptList.append(__import__(localScript.strip('.py')))

		# execute sequentially the scripts
		for script in scriptList:
			script.process()

		return

class JobManager:

	jobList = None
	ressourceWatcher = None

	def __init__(self, sConfigFile):

		self.sConfigFile = sConfigFile
		self.dbConnection = ""

		self.jobList = []

		self.logger = None
		self.initLogging("JobManager")
		self.logger.info("========================================")
		self.logger.info("JobManager in init")

		# check if initfile is valid
		if os.path.exists(self.sConfigFile):
			self.logger.info("init file " + self.sConfigFile + " was found")
			self.configModule = __import__(self.sConfigFile.strip(".py"))

			self.initDbParameters()

			#self.resourceWatcher = ResourceWatcher('atlaslarcal','l1ccalib',15)
			self.resourceWatcher = ResourceWatcher(self.configModule.ResourceWatcher["queue"],self.configModule.ResourceWatcher["account"],self.configModule.ResourceWatcher["joblimit"], self.configModule.ResourceWatcher["ncpu"])

		else:
			self.logger.error("init file "+ self.sConfigFile + " was not found !")
			sys.exit(0)

		self.logger.info("JobManager initialized")
		self.logger.info("========================================")


	def initLogging(self, name):
		#create logger
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.DEBUG)

		#create file handler and set level to debug
		logdir = os.environ['PWD']+'/logs'
		if not os.path.exists(logdir):
			os.mkdir(logdir)
		fh = logging.FileHandler(logdir+'/'+name+'_'+ time.strftime('%Y%m%d_%H%M')+'.log','w')
		fh.setLevel(logging.DEBUG)

		#create formatter
		formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s", datefmt='%Y-%m-%d %H:%M')

		#add formatter to fh
		fh.setFormatter(formatter)

		#add ch to logger
		self.logger.addHandler(fh)


	def initDbParameters(self):
		self.logger.info("retrieveing Db parameters from " + self.sConfigFile + " file")
		self.dbConnection = self.configModule.dbconnection


	def getDbConnection(self):
		return sqlite.connect(self.dbConnection)


	def addNewJobs(self, jobInformationList):
		self.logger.info("Adding new jobs:")
		for jobInfo in jobInformationList:
			job = Job(jobInfo)
			job.resourceWatcher = self.resourceWatcher
			self.jobList.append(job)
			self.logger.info(job.jobInformation.runNumber+"_"+job.jobInformation.jobConfiguration.name)
		return


	def addJobsFromDb(self, jobInformationList):
		self.logger.info("Adding new jobs from Db:")
		print "Adding new jobs from Db:"

		for jobInfo in jobInformationList:
			job = Job(jobInfo)
			job.resourceWatcher = self.resourceWatcher

			job.findRawDataFiles()
			print job.inputRawDataFiles

			if jobInfo.status=='PREPARED':
				print 'status prepared'
				self.logger.info(job.jobInformation.runNumber+"_"+job.jobInformation.jobConfiguration.name+' - '+jobInfo.status)
				#check if files a re still staged
				# if not chag e status
				job.workingAreaStatus = True
				job.isSubmitted = False
				job.isPrepared = True

			if jobInfo.status in ['SUBMITTED', 'PEND', 'RUN']:
				print 'status SUBMITTED PEND RUN'
				self.logger.info(job.jobInformation.runNumber+"_"+job.jobInformation.jobConfiguration.name+' - '+jobInfo.status)
				job.workingAreaStatus = True
				job.isSubmitted = True
				job.isPrepared = True

			self.jobList.append(job)

		return


	def processJobs(self):
		self.logger.debug("from processJobs")

		self.updateJobsStatus()

		for job in self.jobList:
			self.logger.info("=> job: "+job.jobInformation.runNumber+"_"+job.jobInformation.jobConfiguration.name)
			if not job.submitted():
				if not job.prepared():
					self.logger.info("preparing job for submission")
					job.prepareForSubmission()
				else:
					#set state to 'PREPARED'
					self.logger.info("job is prepared - changing status to: PREPARED")
					job.jobInformation.setStatus("PREPARED")

					if self.resourceWatcher.nAvailableJobSlots()>0:
						self.logger.info("bacth slots available - submitting job")
						job.submit()
						#set state to 'SUBMITTED'
						if job.submitted():
							job.jobInformation.setStatus("SUBMITTED")
							self.logger.info("job successfully submitted - new status: "+job.jobInformation.status)
						else:
							print 'error while submitting job'
							#job.jobInformation.setStatus("ABORTED")
							self.logger.info("Error while submitting job - status: "+job.status())
					else:
						self.logger.info("no bacth slots are available")
			else:
				print 'job already submitted'
				self.logger.info("job already submitted - current status: "+job.status())

				if job.jobInformation.status=='DONE':
					self.logger.info("job is 'DONE' ")
					# check job finished without errors from log
					# set 'result' accordingly OK-FAILED
					self.logger.info("checkProcessedOk()")
					job.checkProcessedOk()

					#do post processing
					self.logger.info("posProcessing()")
					#job.postProcess()
					#get number of events, number of warningm errors,...
					# write to report file

					self.logger.info("cleaning working area")
					#clean area, remove *pyc
					Tools.cleanArea(job.jobInformation.jobConfigModule.JobWorkingDir, [".pyc"])

					###==============================###
					self.logger.info("backup to castor")

					castorDir = job.jobInformation.jobConfigModule.JobCastorDir
					if castorDir:
						castorDir +='/'+job.jobInformation.runNumber
						Tools.createCastorFolder(castorDir)

						self.logger.debug(job.jobInformation.jobConfigModule.JobWorkingDir+" -> "+castorDir)
					        #copy to castor if ok
						succeed = Tools.castorFolderCopy(job.jobInformation.jobConfigModule.JobWorkingDir, castorDir, job.jobInformation.jobConfiguration.name)
						if not succeed:
							self.logger.error("Failed to save job data to castor: " + job.jobInformation.jobConfigModule.JobWorkingDir)

					        #create dummy file in dir for space manager
						else:
							cmd = "touch "+ job.jobInformation.jobConfigModule.JobWorkingDir+'/'+"removalok"
							rawoutput = commands.getoutput(cmd)

		# remove from the list the job already done or aborted
		for job in reversed(self.jobList):
				if job.status()=='DONE' or job.status()=='ABORTED':
					self.logger.info("removing job "+job.name() +" with status: "+ job.status())
					self.jobList.remove(job)

		self.logger.debug("end of processJobs")
		return

#		# status NEW -> SENT if jobManager return a batch Id
#		# STAGED/STAGING
#		# PREPARED
#		# SUBMITTED
#		# PENDING
#		# RUNNING
#		# DONE


	def updateJobsStatus(self):
		for job in self.jobList:
			job.updateStatus()
		return


if __name__ == "__main__":
	#x=JobManager("JobOrganizerConfig.py")
	#x.updateJobInformationList()
	print Stager("t0atlas").stage(["/castor/cern.ch/grid/atlas/DAQ/l1calo/0094448/daq.L1CaloTile.0094448.No.Streaming.LB0000.SFI-LVL1-1._0001.data"])

	print Stager("t0atlas").stage(["/castor/cern.ch/grid/atlas/DAQ/l1calo/daq.l1calo.0095469.No.Streaming.LB0000.ROSEventBuilder._0006.data"])


	mlist = ["/castor/cern.ch/user/p/prieur/L1Calo/Commissioning/l1calo/0092512/calib/0092512_calib_0.cbnt",
	"/castor/cern.ch/user/p/prieur/L1Calo/Commissioning/l1calo/0092512/calib/0092512_calib_1.cbnt",
	"/castor/cern.ch/user/p/prieur/L1Calo/Commissioning/l1calo/0092512/calib/0092512_calib_2.cbnt"
	]
	#print Stager().stage(mlist)
