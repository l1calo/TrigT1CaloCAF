#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# usage:

# python submit.py -f/castor/cern.ch/grid/atlas/DAQ/2008/92081/physics_RNDM
# python submit.py -r92081 -sphysics_L1CaloEM
# python submit.py -r92081

# python submit.py -p/castor/cern.ch/grid/atlas/t0/perm/l1calo -r0076807 -scalib --script=athenaCosmicRec_L1CaloOnly.sh
# python submit.py -p/castor/cern.ch/grid/atlas/t0/perm/l1calo -r0076807 -scalib --script=athenaCosmicRec_L1CaloOnly.sh -q1nh

# python submit.py -p/castor/cern.ch/grid/atlas/DAQ/l1calo -r0093436 -scalib --script=athenaCosmicRec_L1CaloOnly.sh -qatlaslarcal -n3
# python submit.py -p/castor/cern.ch/grid/atlas/DAQ/l1calo -r0093436 -scalib --script=athenaCosmicRec_FastCalo.sh -n3

# python submit.py -p/castor/cern.ch/grid/atlas/DAQ/l1calo -r0095574 -scalib --script=athenaCosmicRec_L1CaloOnly.sh -n3

#  python submit.py -p/castor/cern.ch/grid/atlas/DAQ/2009 -r00101719 -sphysics_ptdummy  --script=athenaCosmicRec_FastCalo.sh -qatlaslarcal -n3 --makejoblist

# python submit.py -p/castor/cern.ch/grid/atlas/DAQ/l1calo -r00101856 -scalib  --script=athenaCosmicRec_TileCIS.sh -qatlaslarcal -n3

import os
import sys
import math
from optparse import OptionParser
import commands


#=============================================================#
#     Script to submit reconstruction jobs to LSF             #
#                                                             #
#     damien.prieur@cern.ch                                   #
#=============================================================#

def wait():
	temp = raw_input()
	if len(temp) != 0:
		sys.exit()
	return


def buildDataSetList(path, runNumber, stream, excludeStr):
	if path=='/castor/cern.ch/grid/atlas/t0/perm/l1calo':
		return buildDataSetListFullPath(path, runNumber,excludeStr)
	elif path=='/castor/cern.ch/grid/atlas/DAQ/l1calo':
		if int(runNumber)>=94911 and int(runNumber)<=95575 or int(runNumber)==97374 or int(runNumber)==97287:
			return buildDataSetListFullPath(path, runNumber,excludeStr)
		else:
			return buildDataSetListFullPath(path+'/'+runNumber, runNumber,excludeStr)
	else:
		return buildDataSetListFullPath(path+'/'+runNumber+'/'+stream, runNumber, excludeStr)

def buildDataSetListFullPath(path, runNumber, excludeStr):
	sys.stdout.write("Building datasets list...\n")
	cmd = 'nsls ' + path + ' | grep '+ runNumber
	rawoutput = commands.getoutput(cmd)
	filelist = rawoutput.splitlines()

	triggerfilelist=[]
	for currentfile in filelist:
			if excludeStr!='' and (currentfile.find(excludeStr)!=-1):
				continue
			triggerfilelist.append(currentfile)


	sys.stdout.write("[ok]\n")

	return triggerfilelist

#def submitJob(queue, scriptName, path, inputFile, runNumber, part):
#	fullPath = path + '/' + inputFile
#	dataSetName = inputFile[:-5]
#	jobName = dataSetName+'_'+part
#	cmd = 'bsub -q' + queue + ' -o' + jobName + ' -J' + jobName + ' ' + scriptName + ' '+ fullPath + ' ' + runNumber + ' ' + dataSetName  + ' ' + part
#	os.system(cmd)
#	print queue+' '+jobName+' '+scriptName+' '+runNumber+' '+part
#	return

def submitJob(queue, scriptName, runNumber, triggerStr, part, outputDirectory):
	jobName = runNumber+'_'+str(part)
	cmd = 'bsub -q' + queue + ' -o' + jobName + ' -J' + jobName + ' ' + scriptName + ' ' + runNumber + ' ' + triggerStr + ' ' + str(part) + ' ' + outputDirectory
	os.system(cmd)
	print queue+' '+jobName+' '+scriptName+' '+ runNumber + ' ' + triggerStr + ' ' + str(part) + ' ' + outputDirectory
	return

## create files containing the datasets to be processed by each job and return a list with the job numbers to be submited
def createJobFiles(fileList, options, triggerStr, partList):
	# build the datasetlist files
	dataSetPerJob = int(options.dataSetPerJob)
	nDataSet = len(fileList)
	nJobs = int(math.ceil(float(nDataSet)/float(dataSetPerJob)))

	foutput=[]
	jobNumberList=[]

#	for i in range(nJobs):
#		foutput.append(open(options.outputFilePrefix+options.runNumber+'_'+triggerStr+'_'+str(i)+'.py','w'))
#		foutput[i].write('ATLASCosmicFlags.FullFileName = []\n')
#		jobNumberList.append(i)
#
#	for i in range(nDataSet):
#		ifile = int(math.ceil(i/dataSetPerJob))
#		foutput[ifile].write('ATLASCosmicFlags.FullFileName += [\"'+  options.rawDataPath + '/' + fileList[i] + '\"]\n')
#
#	for i in range(nJobs):
#		foutput[i].close()


# std 13.X.0 intput
#	for i in range(nJobs):
#		if partList!=[]:
#			if str(i) not in partList:
#				continue
#
#		datasetlist =  open(options.outputFilePrefix+options.runNumber+'_'+triggerStr+'_'+str(i)+'.py','w')
#		datasetlist.write('ATLASCosmicFlags.FullFileName = []\n')
#		begindataset = i*dataSetPerJob
#		enddataset = (i+1)*dataSetPerJob
#		for ifile in range(begindataset,enddataset):
#			if ifile<nDataSet:
#				#print str(i)+' '+str(ifile)
#				datasetlist.write('ATLASCosmicFlags.FullFileName += [\"'+  options.rawDataPath + '/' + fileList[ifile] + '\"]\n')
#		datasetlist.close()
#		jobNumberList.append(i)


	for i in range(nJobs):
		if partList!=[]:
			if str(i) not in partList:
				continue

		datasetlist =  open(options.outputFilePrefix+options.runNumber+'_'+triggerStr+'_'+str(i)+'.py','w')
		datasetlist.write('athenaCommonFlags.BSRDOInput = [\n')
		begindataset = i*dataSetPerJob
		enddataset = (i+1)*dataSetPerJob
		for ifile in range(begindataset,enddataset):
			if ifile<nDataSet:
				#print str(i)+' '+str(ifile)
				if options.rawDataPath=='/castor/cern.ch/grid/atlas/DAQ/l1calo':
					if int(options.runNumber)>=94911 and int(options.runNumber)<=95575 or int(options.runNumber)==97374 or int(options.runNumber)==97287:
						datasetlist.write('"'+  options.rawDataPath + '/' + fileList[ifile] + '\",\n')
					else:
						datasetlist.write('"'+  options.rawDataPath +'/' + options.runNumber + '/' + fileList[ifile] + '\",\n')
				else:
					datasetlist.write('"'+  options.rawDataPath  +'/' + options.runNumber +'/' + options.stream + '/' + fileList[ifile] + '\",\n')
		datasetlist.write(']\n')
		datasetlist.close()
		jobNumberList.append(i)
	return jobNumberList

if __name__ == "__main__":

	# Usual verifications and warnings
	if not sys.argv[1:]:
		sys.stdout.write("Sorry: you must specify a run number (-r12345) \n")
		sys.stdout.write("More help avalaible with -h or --help option\n")
		sys.exit(0)

	parser = OptionParser()
	parser.add_option("-r", "--run", action="store", type="string", dest="runNumber",
		help="Specify the run number")

	parser.add_option("-s", "--stream", action="store", type="string", dest="stream",
		help="Specify the stream", default="physics_L1Calo")

	parser.add_option("-o", "--output", action="store", type="string",
		  dest="outputFilePrefix", help="Specify the output files.",default="datasetlist_")

	parser.add_option("--outputdir", action="store", type="string",
		  dest="outputDirectory", help="Specify the output directory",default="/castor/cern.ch/user/l/l1ccalib/reconstruction/calibration/")

	parser.add_option("-f", "--fullpath", action="store", type="string",
		  dest="fullRawDataPath", help="Specify the full path of input datasets",default="")

	parser.add_option("-p", "--path", action="store", type="string",
		  dest="rawDataPath", help="Specify the path of input datasets",default="/castor/cern.ch/grid/atlas/DAQ/2008")

	parser.add_option("-q", "--queue", action="store", type="string",
		  dest="queue", help="Specify the queue",default="atlaslarcal")

	parser.add_option("--script", action="store", type="string",
		  dest="scriptName", help="Specify the script to be executed",default="athenaCosmicRec.sh")

	parser.add_option("-n", "--ndatasetperjob", action="store", type="string",
		  dest="dataSetPerJob", help="Specify the amount of file to be processed per job",default="5")

	parser.add_option("--failedjobs", action="store_true",
	      dest="failedJobs", default=False, help="To re-submit jobs that failed, ie jobs for which the datasetlist_xxx_bxxx_x are still present in the local folder")

	parser.add_option("--makejoblist", action="store_true",
	      dest="makeJobList", default=False, help="To create the datasets list files. No run is submitted when this option is specified")

	parser.add_option("--triggerType", action="store", type="string",
		  dest="triggerType", help="Specify trigger type.", default="")

	parser.add_option("-j", "--joblist", action="store", type="string",
	      dest="jobList", help="file containing the job parts to be processed (only the specified parts will be launched)", default="")

	parser.add_option("-e", "--exclude", action="store", type="string",
	      dest="exclude", help="to exclude file containing the specified string", default="")

	(options, args) = parser.parse_args()

	print options.jobList



## joblist flag
# to read the list of job parts to be launched
# used to filter the part files created in the JobFiles function
	jobNumberFilterList = []
	if(options.jobList!=""):
		filterfile =  open(options.jobList,'r')
		joblist = filterfile.readlines()
		for part in joblist:
			jobNumberFilterList.append(part[:-1])
		#print jobNumberFilterList


## makeJobList flag
#
	if options.makeJobList==True:
		fileList = []
		if options.fullRawDataPath != "":
			sys.stdout.write("\nLooking for runs in folder: "+options.fullRawDataPath+"\n")
			fileList = buildDataSetListFullPath(options.fullRawDataPath, options.runNumber, options.exclude)
		else:
			sys.stdout.write("\nLooking for run: "+options.runNumber +", stream: "+ options.stream + ", in folder: "+options.rawDataPath+"\n")
			fileList = buildDataSetList(options.rawDataPath, options.runNumber, options.stream, options.exclude)
		jobNumberList = createJobFiles(fileList, options, options.stream, jobNumberFilterList)

		print '\n'
		print ' => Processing run ' + options.runNumber
		print ' => ' + str(len(jobNumberList)) + ' job list files created ' + ' ('+str(options.dataSetPerJob)+' datasets per job)'
		print ' => input path: ' + options.rawDataPath
		print '\n'
		sys.exit()


	jobNumberList=[]
## failedJobs flag
# only submit jobs that have failed, ie, jobs for which the local datasetlist_xxxxx_xx.py file is still present
	if options.failedJobs==True:
		#construct the list of local file that failed
		sys.stdout.write("\nLooking for failed job in current folder...\n")
		import glob
		failedJobList = glob.glob('./'+options.outputFilePrefix+options.runNumber+'*.py')

		for job in failedJobList:
			jobNumberList.append(int(job[job.rfind("_")+1:-3]))

		print '\n'
		print ' => Processing run ' + options.runNumber + ' using script ' + options.scriptName
		print ' => Will re-submit ' + str(len(jobNumberList)) + ' jobs to queue ' + options.queue
		print ' => job parts:'
		print jobNumberList
		print ' -> is that ok ? (press return if so)'
		wait()

	else:
## normal running behavior
# dataset list file are created and all the corresponding jobs are submitted

		fileList = []
		if options.fullRawDataPath != "":
			sys.stdout.write("\nLooking for runs in folder: "+options.fullRawDataPath+"\n")
			fileList = buildDataSetListFullPath(options.fullRawDataPath, options.runNumber, options.exclude)
		else:
			sys.stdout.write("\nLooking for run: "+options.runNumber +", stream: "+ options.stream + ", in folder: "+options.rawDataPath+"\n")
			fileList = buildDataSetList(options.rawDataPath, options.runNumber, options.stream, options.exclude)

		jobNumberList = createJobFiles(fileList, options, options.stream, jobNumberFilterList)

		if options.fullRawDataPath != "":
			print '\n'
			print ' => Processing runs from ' + options.fullRawDataPath + ' using script ' + options.scriptName
			print ' => will submit ' + str(len(jobNumberList)) + ' jobs to queue ' + options.queue + ' ('+str(options.dataSetPerJob)+' datasets per job)'
			print ' -> is that ok ? (press return if so)'
			wait()

		else:
			print '\n'
			print ' => Processing run' + options.runNumber + ', stream' + options.stream+ ', using script ' + options.scriptName
			print ' => will submit ' + str(len(jobNumberList)) + ' jobs to queue ' + options.queue + ' ('+str(options.dataSetPerJob)+' datasets per job)'
			print ' => input path: ' + options.rawDataPath
			print ' -> is that ok ? (press return if so)'
			wait()

## submit jobs using run number and jobNumber
	#for i in range(nJobs):
	for part in jobNumberList:
		submitJob(options.queue, options.scriptName, options.runNumber, options.stream, part, options.outputDirectory)
		print options.queue, options.scriptName, options.runNumber, options.stream, part, options.outputDirectory
		#print i

	print '=> Do not delete/modify/overwrite the temporary datasetlist_xxxxxxxx_x.py file until your jobs are done !!!'

