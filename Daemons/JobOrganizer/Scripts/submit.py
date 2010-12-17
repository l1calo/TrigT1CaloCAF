#!/afs/cern.ch/sw/lcg/external/Python/2.5.4/i686-slc5-gcc43-opt/bin/python
###!/usr/bin/env python

import os, shutil, threading, commands


class Listener(threading.Thread):
	def __init__(self, process = ''):
		threading.Thread.__init__(self)
		self.process = process
		self._stopevent = threading.Event( )

	def run(self):
		import time, sys
		naptime = 1
		while not self._stopevent.isSet():
			while True:
				self.process.fromchild.flush()
				line = self.process.fromchild.readline()
				if not line:
					break
				print line[:-1]
			time.sleep(naptime)
			#if self.process.poll != -1:
			#	self.stop()

	def stop(self):
		self._stopevent.set( )


def copyFile(inputPath, outputPath):
	#add something to handle castor

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

def launchAthena(athenaLauncher):

	# launch Athena
	import popen2
	cmd = 'source ./' + athenaLauncher
	child = popen2.Popen4(cmd)

	a = Listener(child)
	child.tochild.close()
	a.start()
	child.wait()
	a.stop()

	status = child.fromchild.close()
	if status is not None:
		print "status: ", status


if __name__ == "__main__":

	#copy the content of the 'config' folder to local run area
	shutil.copytree("#JOB_CONFIG_DIR#", os.environ["PWD"]+'/run')

	#move to the 'run' dir
	os.chdir('./run')

	# get name of job configuration
	cfPath, cfName = os.path.split("#JOB_CONFIGURATION_LOCAL#")

	print cfPath, cfName

	# load the config file
	cfModule = __import__(cfName.strip(".py"))

	launchAthena(cfModule.AthenaLauncher)


	# do post processing if needed
	for status, cmds in cfModule.JobPostTreatments.items():
	        for cmd in cmds:
	                rawoutput = commands.getoutput(cmd)
	                print cmd
	                print rawoutput


	# copy back output files
	for fileName, destinations in cfModule.OutputFiles.items():
		for dest in destinations:
			copyFile(fileName, dest[0]+'/'+dest[1])

