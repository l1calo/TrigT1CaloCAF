#!/usr/bin/env python

import os, logging, sys, commands, time
import smtplib
from email.MIMEText import MIMEText

class W0Monitor:

	configModule = None

	def __init__(self, sConfigFile):

		self.sConfigFile = sConfigFile

		self.dbConnection = ""

		self.logger = None
		self.initLogging("W0Monitor")

		self.logger.info("========================================")
		self.logger.info("W0Monitor in init")

		# check if initfile is valid
		if os.path.exists(self.sConfigFile):
			self.logger.info("init file " + self.sConfigFile + " was found")

			# sConfigFile has to be a LOCAL PATH (ie ./blabla), because __import__ does not support
			# the 'cern.ch' in the absolute paths (ie /afs/cern.ch)
			self.configModule = __import__(self.sConfigFile.strip(".py"))

		else:
			self.logger.error("init file "+ self.sConfigFile + " was not found !")
			sys.exit(0)

		self.logger.info("Watching at: " + self.configModule.W0Path)
		self.logger.info("Purge threshold: " + str(self.configModule.W0PurgeThreshold)+'%')
		self.logger.info("RemovalOk: " + str(self.configModule.RemovalOk))
		currentUsage = self.quota(self.configModule.W0Path)
		self.logger.info("current usage : "+str(currentUsage)+'%')
		self.logger.info("W0Monitor initialized")
		self.logger.info("========================================")

		return


	def initLogging(self, name):
		#create logger
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.DEBUG)

		#create file handler and set level to debug
		logdir = os.environ['PWD']+'/logs/'
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


	def quota(self, path):

		cmd =  "fs quota "+ path
		rawOutput = commands.getoutput(cmd)
		return int(rawOutput[:rawOutput.find("%")])


	def monitor(self):

		currentUsage = self.quota(self.configModule.W0Path)
		print self.configModule.W0PurgeThreshold

		#self.logger.info("current usage of "+self.configModule.W0Path+": "+str(currentUsage)+'%')
		if currentUsage>self.configModule.W0PurgeThreshold:
			self.purgeArea()


	def purgeArea(self):
		print 'purgeArea'
		self.logger.info("purging "+self.configModule.W0Path+" ...")

		date_folder_list = []

		# build a list of tuple (date, size, path)
		for folder in os.listdir(self.configModule.W0Path):

			folderPath = self.configModule.W0Path+'/'+folder

			# is ok to be removed ?
			if self.configModule.RemovalOk:
				if not os.path.exists(folderPath+'/removalok'):
					continue

			cmd = 'du -sk '+ folderPath
			rawOutput = commands.getoutput(cmd).split()
			size = rawOutput[0]

			#cmd = 'du -sk '+ folderPath
			#rawOutput = commands.getoutput(cmd).split()

			stats = os.stat(folderPath)

			lastmod_date = time.localtime(stats[8])
			date_folder_tuple = lastmod_date, size, folderPath
			date_folder_list.append(date_folder_tuple)

		# sort list by date
		date_folder_list.sort()

#		for folder in date_folder_list:
#			path, name = os.path.split(folder[2])
#			folder_date = time.strftime("%m/%d/%y %H:%M:%S", folder[0])
#			folder_size = folder[1]
#			print "%-40s %s %s" % (name, folder_size, folder_date)

		quota = self.quota(self.configModule.W0Path)
		while quota >self.configModule.W0PurgeThreshold:
			if len(date_folder_list)!=0:
				path = date_folder_list[0][2]
				print 'path to remove: ', path
				#cmd = 'rm -r ' + path
				#rawOutput = commands.getoutput(cmd)
				date_folder_list.pop(0)

				quota = self.quota(self.configModule.W0Path)
				self.logger.info(path+" removed. New quota: "+str(quota)+"%")
			else:
				self.logger.warning("No more folders to remove but quota is still above threshold: "+str(quota)+ '% ('+str(self.configModule.W0PurgeThreshold)+'%)')
				# send email !
				subject = "W0Monitor Warning"
				message = "No more folders to remove but quota is still above threshold: "+str(quota)+ '% ('+str(self.configModule.W0PurgeThreshold)+'%)'
				self.sendTextMail(subject, message, self.configModule.MailingList)
				break

		return


	def sendTextMail(self, sSubject, sText, sMailingList):

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



if __name__ == "__main__":
	x = W0Monitor("W0MonitorConfig.py")
	x.monitor()
