#!/usr/bin/env python

import os, logging, sys
import xml.dom.minidom
from xml.dom.minidom import Node
import sqlite3 as sqlite

#from RunsProvider import RunInformation
from Tools import *
from JobManager import *


# copied from  RunsProvider
class RunInformation:
	runNumber = None
	runParameters = None
	runListenerName = None
	validated = None
	rawPath = None

	def __init__(self):
		self.runNumber = ""
		self.runParameters = None
		self.runListenerName = ""
		self.validated = False
		self.rawPath = ""

	def __str__(self):
		return 'run: '+str(self.runNumber)+', runListener: '+str(self.runListenerName)+', validated: '+str(self.validated)


class JobConfiguration:
	name = None
	listeners = []
	configurationTemplate = None

	#JobManager

	validateRun = None
	validateJob = None

	def __init__(self):
		self.name = ""
		self.listeners = []
		self.configurationTemplate = ""

		self.validateRun = True
		self.validateJob = True


	def __str__(self):
		tmp = 'name: '+str(self.name)+', listeners: '
		for l in self.listeners:
			tmp = tmp + str(l)+' '
		tmp = tmp + 'jo: '+str(self.jobOption)+ ', inputPath: '+str(self.inputPath)+', outputPath: '+str(self.outputPath)
		return tmp

	def suits(self, runInfo):
		for listener in self.listeners:
			if listener==runInfo.runListenerName:
				return True
		return False

#class RunSet:

class JobInformation:
	runNumber=None
	jobConfiguration=None

	placeHolders = {}
	jobConfigModule = None
	jobConfigModulePath = None

	status=None
	batchid=None
	result=None
	validation=None
	rawPath=None

	jobStart=None
	jobEnd=None

	def __init__(self):
		self.runNumber=None
		self.jobConfiguration=None
		self.placeHolders = {}
		self.jobConfigModule = None
		self.jobConfigModulePath = ""
		self.status=""
		self.batchid=""
		self.result=""
		self.validation=""
		self.dbConnection = ""
		self.rawPath=""
		self.jobStart=None
		self.jobEnd=None


	def __str__(self):
		tmp = str(self.runNumber)+' '+ str(self.jobConfiguration.name)+' '+ str(self.status)+' '+ str(self.batchid)+' '+ str(self.result)+' '+ str(self.validation)
		return tmp

	def loadConfigModule(self):

		#copy
		if self.jobConfiguration.configurationTemplate!="":
			self.jobConfigModule = __import__(self.jobConfiguration.configurationTemplate.strip(".py"))
		return

	def setStatus(self, newStatus):
		#print newStatus, self.status
		if newStatus!=self.status:
			self.status = newStatus
			self.updateJobDb("status", str(newStatus))
		return

	def setBatchId(self, newId):
		if newId!=self.batchid:
			self.batchid = newId
			self.updateJobDb("batchid", str(newId))
		return

	def setResult(self, result):
			self.result = result
			self.updateJobDb("result", str(result))
			return

	def setStartTime(self, stime):
		self.jobStart = stime
		self.updateJobDb("jobstart", str(stime))
		return

	def setStopTime(self, stime):
		self.jobEnd = stime
		self.updateJobDb("jobend", str(stime))
		return

	def updateJobDb(self, attribute, value):
		connection = sqlite.connect(self.dbConnection)
		cursor = connection.cursor()
		cursor.execute("update JOBSTATUS set "+str(attribute)+"=? where run=? AND jobconfiguration=?",(value, str(self.runNumber), str(self.jobConfiguration.name)))
		connection.commit()
		connection.close()
		return

class JobOrganizer:

	jobInformationList = []
	jobConfigurationList = {}
	#runSetList = []
	configModule = None
	jobManager = None

	def __init__(self, sConfigFile):

		self.sConfigFile = sConfigFile

		self.dbConnection = ""

		self.logger = None
		self.initLogging("JobOrganizer")
		self.logger.info("========================================")
		self.logger.info("JobOrganizer in init")


		# check if initfile is valid
		if os.path.exists(self.sConfigFile):
			self.logger.info("init file " + self.sConfigFile + " was found")
			self.configModule = __import__(self.sConfigFile.strip(".py"))

			#self.createRunlisteners()
			#self.initRunListeners()
			self.initDbParameters()
			self.readJobsConfiguration()

			self.jobManager = JobManager(self.sConfigFile)

			Tools.createFolder('tmp/jobConfig')

		else:
			self.logger.error("init file "+ self.sConfigFile + " was not found !")
			sys.exit(0)

		self.logger.info("JobOrganizer initialized")
		self.logger.info("========================================")


	def initLogging(self, name):
		#create logger
		self.logger = logging.getLogger(name)
		#self.logger.setLevel(logging.DEBUG)
		self.logger.setLevel(logging.INFO)

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


	def readJobsConfiguration(self):

		self.logger.info("creating job configurations from " + self.sConfigFile + " file")

		self.jobConfigurationList = {}

		for name, jobConfig in self.configModule.jobConfigurations.items():
			jc = JobConfiguration()

			jc.name = name
			jc.configurationTemplate = jobConfig["configurationTemplate"]
			jc.listeners = jobConfig["listeners"]
			jc.validateJob = jobConfig["validateJob"]

			self.jobConfigurationList[name] = jc


	def initDbParameters(self):
		self.logger.info("retrieveing Db parameters from " + self.sConfigFile + " file")
		self.dbConnection = self.configModule.dbconnection


	def getDbConnection(self):
		return sqlite.connect(self.dbConnection)

	def getNewRunsFromDb(self):

		# connect to DB
		connection = self.getDbConnection()

		cursor = connection.cursor()
		# we retrieve only the new runs with rawstatus = 'OK' ie when all datasets are available
		cursor.execute("select run, listener, validated, rawpath from RUNSTATUS where status='NEW'") # and rawstatus='OK'

		#build a list of runs from Db
		runsFromDb = []
		for row in cursor:
			ri = RunInformation()
			ri.runNumber = str(row[0])
			ri.runListenerName = str(row[1])
			if str(row[2])=="True":
				ri.validated = True
			ri.rawPath = str(row[3])
			runsFromDb.append(ri)

		connection.close()
		return runsFromDb


	def loadJobConfigModule(self, jobInformation):

		sConfigTpl = jobInformation.jobConfiguration.configurationTemplate
		#placeHolders = {}
		jobInformation.placeHolders['#RUN_NUMBER#'] = str(jobInformation.runNumber)
		jobInformation.placeHolders['#RUN_NUMBER_PADDED#'] = runNumberToStr(int(jobInformation.runNumber))
		jobInformation.placeHolders['#RUN_NUMBER_PADDED_8#'] = '0'+runNumberToStr(int(jobInformation.runNumber))

		jobInformation.placeHolders['#JOB_CONFIGURATION#'] = str(jobInformation.jobConfiguration.name)

		jobInformation.placeHolders['#DAEMON_JO_TEMPLATE_DIR#'] = str(self.configModule.JobOptionsTemplateDir)
		jobInformation.placeHolders['#DAEMON_SCRIPTS_DIR#'] = str(self.configModule.ScriptsDir)
		jobInformation.placeHolders['#DAEMON_BACKENDS_DIR#'] = str(self.configModule.BackEndsDir)

		jobInformation.placeHolders['#JOBS_WORKING_DIR#'] = str(self.configModule.JobsWorkingDir)


		jobWorkingDir = str(self.configModule.JobsWorkingDir)+'/'+str(jobInformation.runNumber)+'_'+str(jobInformation.jobConfiguration.name)
		jobLogDir = jobWorkingDir + '/log'
		jobRootDir = jobWorkingDir + '/root'
		jobPoolDir = jobWorkingDir + '/pool'
		jobConfigDir = jobWorkingDir + '/config'
		jobPostDir = jobWorkingDir + '/post'

		jobInformation.placeHolders['#JOB_WORKING_DIR#'] = jobWorkingDir
		jobInformation.placeHolders['#JOB_LOG_DIR#'] = jobLogDir
		jobInformation.placeHolders['#JOB_ROOT_DIR#'] = jobRootDir
		jobInformation.placeHolders['#JOB_POOL_DIR#'] = jobPoolDir
		jobInformation.placeHolders['#JOB_CONFIG_DIR#'] = jobConfigDir
		jobInformation.placeHolders['#JOB_POST_DIR#'] = jobPostDir

		jobInformation.placeHolders['#CASTOR_DATA_DIR#'] = self.configModule.CastorDataDir


		#get configtpl

		sConfigModule = str(jobInformation.runNumber)+'_'+str(jobInformation.jobConfiguration.name)+'_jobConfig.py'
		sInputPath = self.configModule.ConfigTemplateDir+'/'+sConfigTpl

		#need to check or create folders
		#sOutputPath = self.configModule.TmpInstallDir+'/jobConfig/'+sConfigModule
		sOutputPath = 'tmp/jobConfig/'+sConfigModule
		#sOutputPath = os.environ['PWD']+'/tmp/jobConfig'
		#jobInformation.jobConfigModulePath = sOutputPath+'/'+sConfigModule
		jobInformation.jobConfigModulePath = sOutputPath

		#replaceTag(sInputPath, jobInformation.jobConfigModulePath, jobInformation.placeHolders)
		replaceTag(sInputPath, sOutputPath, jobInformation.placeHolders)

		#print sOutputPath
		#os.chdir(sOutputPath)
		jobInformation.jobConfigModule = __import__(sOutputPath.strip(".py"))
		#jobInformation.jobConfigModule = __import__('tmp/jobConfig/'+sConfigModule.strip(".py"))

		return


	def initJobInformationListFromDb(self):

		connection = self.getDbConnection()
		cursor = connection.cursor()

		cursor.execute('select run, jobconfiguration, batchid, status, validation, rawpath, jobstart, jobend from JOBSTATUS where validation="WAITING" OR ((validation="YES" OR validation="NONE") AND status<>"DONE")')
		for row in cursor:

			if row[1] in self.jobConfigurationList.keys():
				jobInfo = JobInformation()

				jobInfo.runNumber = row[0]
				jobInfo.jobConfiguration = self.jobConfigurationList[row[1]]
				jobInfo.batchid = row[2]
				jobInfo.status = row[3]
				jobInfo.validation = row[4]
				jobInfo.rawPath = row[5]
				jobInfo.jobStart = row[6]
				jobInfo.jobEnd = row[7]
				jobInfo.dbConnection = self.dbConnection

				self.loadJobConfigModule(jobInfo)

				self.jobInformationList.append(jobInfo)


#		for jobInfo in self.jobInformationList:
#			print jobInfo

		connection.close()

		#send list of jobs not NEW to jobManager
		jobList = []
		for jobInfo in self.jobInformationList:
			if jobInfo.status!='NEW':
				jobList.append(jobInfo)

		self.jobManager.addJobsFromDb(jobList)
		return

	def newJobsFromDb(self):
		jobList = []

		connection = self.getDbConnection()
		cursor = connection.cursor()

		cursor.execute('select run, jobconfiguration, batchid, status, validation, rawpath, jobstart, jobend from JOBSTATUS where validation="WAITING" OR ((validation="YES" OR validation="NONE") AND status<>"DONE")')
		for row in cursor:

			if row[1] in self.jobConfigurationList.keys():
				jobInfo = JobInformation()

				jobInfo.runNumber = row[0]
				jobInfo.jobConfiguration = self.jobConfigurationList[row[1]]
				jobInfo.batchid = row[2]
				jobInfo.status = row[3]
				jobInfo.validation = row[4]
				jobInfo.rawPath = row[5]
				jobInfo.jobStart = row[6]
				jobInfo.jobEnd = row[7]
				jobInfo.dbConnection = self.dbConnection

				self.loadJobConfigModule(jobInfo)

				jobList.append(jobInfo)

		return jobList

	def updateJobInformationList(self):

		connection = self.getDbConnection()
		cursor = connection.cursor()

		self.logger.info("Updating jobInformation list")

		###================================###
		# get list of new runs from the run Db
		runInfoList = self.getNewRunsFromDb()

		if runInfoList!=[]:
			self.logger.debug("-> New runs found in run DB:")

			# associate a jobConfigutation
			for runInfo in runInfoList:
				self.logger.debug(" * run "+runInfo.runNumber)

				for name, jobConfig in self.jobConfigurationList.items():
					if jobConfig.suits(runInfo):

	#					# if the jobConfig requires the run to be validated and that one is not
	#					# the job is not considered
	#					if jobConfig.validateJob:
	#						print 'tutu'
	#						if not runInfo.validated:
	#							continue

						#sould consider the number of files and create as many sub-jobs as needed
						# depending on jobConfiguration
						# jobInfo.subjob=1,2,3,...

						# create a new jobInformation
						jobInfo = JobInformation()
						jobInfo.dbConnection = self.dbConnection
						jobInfo.runNumber = runInfo.runNumber
						jobInfo.rawPath = runInfo.rawPath
						jobInfo.jobConfiguration = jobConfig
						self.loadJobConfigModule(jobInfo)

						jobInfo.status = 'NEW'

						needsValidation = (jobConfig.validateJob or runInfo.validated)
						self.logger.info("validate job: "+str(needsValidation))
						if needsValidation:
						        jobInfo.validation = 'WAITING'
						else:
						        jobInfo.validation = 'NONE'

						self.logger.info("jobInfo.validation: "+jobInfo.validation)

						#check db to see if no run/jobconfig already there
						cursor.execute('select run, jobconfiguration from JOBSTATUS')
						alreadyInJobDb = False
						for row in cursor:
							if row[0]==str(jobInfo.runNumber) and row[1]==str(jobInfo.jobConfiguration.name):
								alreadyInJobDb = True
								break

						if not alreadyInJobDb:
							self.jobInformationList.append(jobInfo)
							cursor.execute("insert into JOBSTATUS(id, run, jobconfiguration, status, validation) values (null, ?, ?, ?, ?)", (jobInfo.runNumber, jobInfo.jobConfiguration.name, jobInfo.status, jobInfo.validation))
							self.logger.info(jobInfo.runNumber+'_'+jobInfo.jobConfiguration.name+" added to jobInformation list")

						else:
							self.logger.info(jobInfo.runNumber+'_'+jobInfo.jobConfiguration.name+" already exist in the job DB")


				# set run as 'seen' in runstatus DB
				cursor.execute("update RUNSTATUS set status=? where run=?",('OK',str(runInfo.runNumber)))

			connection.commit()

		else:
			self.logger.debug("-> No new runs found in run DB")

		###===============================================================###
		# check job with status = NEW that are not in current job list
		# ie job modified by external progs after the deamon start
		# reprocess attribute ?

		self.logger.debug("looking for new jobs in job DB")

		newJobs = self.newJobsFromDb()
		for newJob in newJobs:
			alreadyInJobList = False
			for jobInfo in self.jobInformationList:
				if str(jobInfo.runNumber)==str(newJob.runNumber) and str(jobInfo.jobConfiguration.name)==str(newJob.jobConfiguration.name):
					alreadyInJobList=True
					break
			if not alreadyInJobList:
				self.jobInformationList.append(newJob)
				self.logger.debug("job "+jobInfo.runNumber+'_'+jobInfo.jobConfiguration.name+" added to jobInformation list")

			else:
				self.logger.debug("job "+jobInfo.runNumber+'_'+jobInfo.jobConfiguration.name+" already in jobInformation list")


		###===============================================================###
		# update validation state from DB for jobs with validation=WAITING
		for jobInfo in self.jobInformationList:
			if jobInfo.validation=="WAITING":
				cursor.execute('select validation from JOBSTATUS where run=? and jobconfiguration=?',(jobInfo.runNumber, jobInfo.jobConfiguration.name))
				jobInfo.validation = cursor.fetchone()[0]


		###=============================###
		# update job status from JobManager
		self.jobManager.updateJobsStatus()


		###===========================================================###
		# remove job DONE or validation=BAD from  self.jobInformationList
		# do not touch the DB
		for jobInfo in reversed(self.jobInformationList):
			if jobInfo.validation=="BAD" or jobInfo.status=="DONE":

				self.logger.debug("removing jobInformation "+jobInfo.runNumber+'_'+jobInfo.jobConfiguration.name+ ", status: "+jobInfo.status+", validation: "+jobInfo.validation)

				#delete the jobInfo associated config file
				cmd = 'rm '+jobInfo.jobConfigModulePath.strip('.py')+'.*'
				commands.getoutput(cmd)

				#remove jobInfo form list
				self.jobInformationList.remove(jobInfo)

		connection.close()

		return


	def submitBatchJobs(self):

		jobInfoList=[]

		#select jobs to be processed (is validated==NONE or YES? is set/dependencies complete ?)
		for jobInfo in self.jobInformationList:
			if (jobInfo.validation=="NONE" or jobInfo.validation=="YES") and jobInfo.status=="NEW":
				jobInfoList.append(jobInfo)

		#print jobInfoList
		self.jobManager.addNewJobs(jobInfoList)

		return


	def processBatchJobs(self):
		self.jobManager.processJobs()
		return

#	def updateBatchJobs(self):
#		#update the status attribute of self.jobInformationList from jobManager
#
#		# status NEW -> SENT if jobManager return a batch Id
#		# STAGING
#		# PREPARED
#		# SUBMITTED
#		# PENDING
#		# RUNNING
#		# DONE
#
#		#also update jobDb
#		return


if __name__ == "__main__":
	#x=JobOrganizer("joborganizer.xml")
	x=JobOrganizer("JobOrganizerConfig.py")

	x.initJobInformationListFromDb()
	x.updateJobInformationList()
	x.submitBatchJobs()
	x.processBatchJobs()
	x.processBatchJobs()

