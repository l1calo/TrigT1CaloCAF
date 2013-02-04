#!/usr/bin/env python

import sys, time, os, commands
from Daemon import Daemon
from JobOrganizer import JobOrganizer

class JobOrganizerDaemon(Daemon):
	def __init__(self, pidfile, stdin='/dev/null', stdout='/tmp/l1ccalib/jobOrgStd.txt', stderr='/tmp/l1ccalib/jobOrgErr.txt'):
		Daemon.__init__(self, pidfile, stdin, stdout, stderr)

	def run(self):

		# the demaon chdir to '/' before the call to runtime_error
		# W0Monitor expect a local path to its config file, so we chdir to where
		# the config file is
		os.chdir(os.environ["PWD"])
		self.jobOrganizer = JobOrganizer("JobOrganizerConfig.py")
		self.jobOrganizer.initJobInformationListFromDb()
		#os.chdir('/')

		#sys.stdout.flush()
		#sys.stderr.flush()
		cmd = 'klist'
		rawoutput = commands.getoutput(cmd)
		print rawoutput
		cmd = 'tokens'
		rawoutput = commands.getoutput(cmd)
		print rawoutput
		sys.stdout.flush()

		while True:
			self.jobOrganizer.updateJobInformationList()
			self.jobOrganizer.submitBatchJobs()
			self.jobOrganizer.processBatchJobs()
			time.sleep(120)

if __name__ == "__main__":
	daemon = JobOrganizerDaemon(os.environ["PWD"]+'/joborganizerdaemon.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'foreground' == sys.argv[1]:
			daemon.run()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|foreground" % sys.argv[0]
		sys.exit(2)
