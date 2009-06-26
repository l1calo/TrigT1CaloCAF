#!/usr/bin/env python

import os, commands, string, shutil, glob
import os.path

from os.path import exists


def replaceTagInString(inputStr, placeHolders):
	outputStr = ''

	for s in inputStr:
		for ph in placeHolders:
			s=s.replace(ph, placeHolders[ph])
		outputStr=outputStr+s

	return outputStr


def replaceTag(inputfile, outputfile, placeHolders):

	#check is input path is valid and is really a file
	if not exists(inputfile) or not os.path.isfile(inputfile):
		print 'input file not found: ' + inputfile
		return False

	# if output path is a valid dir, the output file will have the same name as the input one
	if os.path.isdir(outputfile):
		outputfile = outputfile.rstrip('/')+'/'+ os.path.split(inputfile.rstrip('/'))[1]
		#print outputfile

	output_class = open(outputfile,'w')
	input_template = open(inputfile)

	for s in input_template:
		for ph in placeHolders:
			s=s.replace(ph, placeHolders[ph])
		output_class.write(s)

	output_class.close()
	input_template.close()

	if not os.path.isfile(outputfile):
		return False

	return True


def listFiles(path, grepStr=""):
	#print 'listFiles:'
	cmd=""
	if grepStr=="":
		cmd = 'nsls ' + path
	else:
		cmd = 'nsls ' + path + ' | grep '+ grepStr

	rawoutput = commands.getoutput(cmd)
	if 'No such file or directory' in rawoutput:
		return []
	filelist = rawoutput.splitlines()

	#print rawoutput

	pathList=[]
	for fi in filelist:
		pathList.append(path+'/'+fi)

	return pathList


def runNumberToStr(runNumber):
	return "%.7d" % (runNumber)


def createFolder(path):
	if path!="" and not exists(path):
		try:
			#os.mkdir(path)
			os.makedirs(path)
		except:
			return False
	return True


def copyFile(inputPath, outputPath):
	if not os.path.isfile(inputPath):
		print 'input file not found: '+inputPath
		return False

#	if not exists(outputPath):
#		print 'output file not found: '+outputPath

	try:
		shutil.copy(inputPath, outputPath)

	except:
		print 'problem when copying: '+inputPath+' to: '+outputPath
		return False

	return True


def checkProcessedOk(path):

	#open log file
	if not exists(path):
		print 'log file not found: ' + path
		return False

	processedOk = False
	logFile = open(path)
	for line in logFile:
		if 'leaving with code 0: "successful run"' in line:
			processedOk = True
			break

	# count number of events must >0
	return processedOk

def listFilesRecursive(path):
    fichier=[]
    for root, dirs, files in os.walk(path):
        for i in files:
            fichier.append(os.path.join(root, i))
    return fichier

def listFoldersRecursive(path):
    folders=[]
    for root, dirs, files in os.walk(path):
        for i in dirs:
            folders.append(os.path.join(root, i))
    return folders

def createCastorFolder(path):
	cmd='rfmkdir '+path
	print cmd
	rawoutput = commands.getoutput(cmd)
	#print rawoutput
	return True

def castorFolderCopy(inputPath, outputPath, rename=""):

	outputPath = outputPath.rstrip('/')
	inputPath = inputPath.rstrip('/')

	inputFolderName = os.path.split(inputPath)[1]
	if rename!="":
		inputFolderName = rename

	fileList = listFilesRecursive(inputPath)
	folderList = listFoldersRecursive(inputPath)

	outputFolderPath = outputPath+'/'+inputFolderName

	bStatus = True

	#create directory structure
	createCastorFolder(outputFolderPath)
	for folder in folderList:
		bStatus &= createCastorFolder(folder.replace(inputPath, outputFolderPath))
	print 'createCastorFolder: ', bStatus

	# copy files
	for ifile in fileList:
		dest = os.path.split(ifile)[0].replace(inputPath, outputFolderPath)
		bStatus &= safeRfcp(ifile, dest)
		if not bStatus:
			print "pb copying: ", ifile, dest

	return bStatus

def safeRfcp(inputfile, outputpath):

	outputpath = outputpath.rstrip('/')

	#rfcp
	cmd='rfcp '+inputfile+' '+outputpath
	rawoutput = commands.getoutput(cmd)
	print rawoutput

	# check size
	inputSize = getSize(inputfile)
	outputSize = getSize(outputpath+'/'+os.path.split(inputfile)[1])

	return inputSize==outputSize

#-----------------------------------------------------------------------
# determine size of a local file
#-----------------------------------------------------------------------
def getSize(name) :
  size = long(12345678)
  if '/castor/' in name:
	(s,o) = commands.getstatusoutput('nsls -l %s' % name)
  else:
	(s,o) = commands.getstatusoutput('/bin/ls -l %s' % name)
  if s == 0 : size = long(o.split()[4])

  return size


def cleanArea(path, patternList):
	fileList = listFilesRecursive(path)

	for ifile in fileList:
		for pattern in patternList:
			if pattern in ifile:
				#print ifile
				os.remove(ifile)

	return


def sendTextMail(sSubject, sText, sMailingList):

	sFrom = os.environ["USER"]+" <"+os.environ["USER"]+"@cern.ch>"
	sTo=""
	for x in sMailingList: sTo=sTo+x+";"

	mail = MIMEText(sText)
	mail['From'] = sFrom
	mail['Subject'] = sSubject
	mail['To'] = sTo

	smtp = smtplib.SMTP()
	smtp.connect()
	smtp.sendmail(sFrom, sMailingList, mail.as_string())
	smtp.close()
	return

#  def Tools_CheckDiskQuota(self,sWorkingDirectory, sWarningList):
#
#        if sWorkingDirectory[0:4]=="/afs":
#            sCommand="fs listquota"
#            sRes=self.Tools_ExecuteCommand(sCommand,COMMAND_WARNING)
#            sLine=sRes[1].split('\n')[1]
#            sElement=[x for x in sLine.split(' ') if x!='']
#
#            sDiskSpace=int(sElement[1])-int(sElement[2])
#
#            if sDiskSpace<5000 :
#                sText="Only "+str(sDiskSpace)+" Mo left for reconstruction daemon "+sWorkingDirectory
#                self.Tools_SendTextMail(sWarningList,os.environ["USER"]+" disk space problem ",sText)





if __name__ == "__main__":
		#print glob.glob('/afs/cern.ch/user/p/prieur/w0/DaemonData/jobs/94448_CBNT/*/*')
		#print listFoldersRecursive('/afs/cern.ch/user/p/prieur/w0/DaemonData/jobs/94448_CBNT')
		#print listFilesRecursive('/afs/cern.ch/user/p/prieur/w0/DaemonData/jobs/94448_CBNT')
		#castorFolderCopy('/afs/cern.ch/user/p/prieur/w0/DaemonData/jobs/94448_CBNT','/castor/cern.ch/user/p/prieur/L1Calo/Commissioning/l1calo')
		#castorFolderCopy('/afs/cern.ch/user/p/prieur/w0/DaemonData/jobs/94448_CBNT','/tmp/prieur')
		cleanArea('/afs/cern.ch/user/p/prieur/w0/DaemonData/jobs/94448_CBNT',[".pyc"])


