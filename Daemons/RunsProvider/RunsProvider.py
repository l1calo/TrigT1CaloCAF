#!/usr/bin/env python

import os, logging, time
from RunListener import RunListener
import sqlite3 as sqlite

import Tools

import smtplib
from email.MIMEText import MIMEText

class RunInformation:
    runNumber = None
    runParameters = None
    runListenerName = None
    validated = None
    rawPath = None
    nFiles=None
    rawStatus=None

    def __init__(self):
        self.runNumber = ""
        self.runParameters = None
        self.runListenerName = ""
        self.validated = False
        self.rawPath = ""
        self.nFiles = 0
        self.rawStatus = ""

    def __str__(self):
        return 'run: '+str(self.runNumber)+', runListener: '+str(self.runListenerName)+', validated: '+str(self.validated)


class RunsProvider:

    __runListenersList__ = None
    config = None

    def __init__(self, sConfigFile):

        self.sConfigFile = sConfigFile
        self.__runListenersList__ = []
        self.dbConnection = ''

        self.logger = None
        self.initLogging("RunsProvider")

        self.logger.info("========================================")
        self.logger.info("RunsProvider in init")

        # check if initfile is valid
        if os.path.exists(self.sConfigFile):
            self.logger.info("init file " + self.sConfigFile + " was found")

            # sConfigFile has to be a LOCAL PATH (ie ./blabla), because __import__ does not support
            # the 'cern.ch' in the absolute paths (ie /afs/cern.ch)
            self.config = __import__(self.sConfigFile.strip(".py"))

            self.createRunlisteners()
            self.initRunListeners()
            self.initDbParameters()

        else:
            self.logger.error("init file "+ self.xmlInitFile + " was not found !")
            sys.exit(0)

        self.logger.info("RunsProvider initialized")
        self.logger.info("========================================")


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


    def isInitialized(self):
        return self.__runListenersList__ != []

    def getText(self, node):
        return str(node.childNodes[0].nodeValue)

    def getTextSafe(self, node):
        tmp=""
        try:
            tmp = self.getText(node)
        except:
            tmp==""
        return tmp

    def stringToBool(self, string):
        if string=="True":
            return True
        elif string =="False":
            return False
        else:
            return None

    def createRunlisteners(self):

        self.logger.info("creating run listeners from " + self.sConfigFile + " file")

        for name, options in self.config.runListeners.items():
            rl = RunListener(name)
            rl.tdaqdbname = options["tdaqdbname"]
            rl.trigdbname = options["trigdbname"]
            rl.statusdbname = options["statusdbname"]
            rl.loglevel = options["loglevel"]
            rl.oracle = options["oracle"]
            rl.reconly = options["reconly"]
            rl.detmask = options["detmask"]
            rl.runtype = options["runtype"]
            rl.tag = options["tag"]
            rl.detstatus = options["detstatus"]
            rl.detstatustag = options["detstatustag"]
            rl.daqpartition = options["daqpartition"]
            rl.tierzerotag = options["tierzerotag"]
            rl.NOTtierzerotag = options["NOTtierzerotag"]

            rl.format = options["format"]
            rl.reverse = options["reverse"]

            rl.stoptimestamp = options["stoptimestamp"]
            rl.cleanstop = options["cleanstop"]
            rl.hasevents = options["hasevents"]
            rl.minevents = options["minevents"]

            rl.initialRun =  options["initialrun"]
            # if ==0, then get last run from DB

            rl.fileslocations = options["fileslocations"]


            # add it to the list of runListeners
            self.__runListenersList__.append(rl)
            self.logger.info(name + " added to the list of run listeners")


    def initRunListeners(self):
        for rl in self.__runListenersList__:
            rl.initRunListener()


    def initDbParameters(self):

        self.logger.info("retrieveing Db parameters from " + self.sConfigFile + " file")
        self.dbConnection = self.config.dbConnection


    def getDbConnection(self):
        return sqlite.connect(self.dbConnection)


    def replaceTagInString(self, inputStr, placeHolders):
        for ph in placeHolders:
            inputStr =inputStr.replace(ph, placeHolders[ph])
        return inputStr

    def runNumberToStr(self, runNumber):
        return "%.7d" % (runNumber)

    def findRawDataFiles(self, runListener, runNumber):
        phDict={}
        phDict["#RUN_NUMBER_PADDED#"] = self.runNumberToStr(int(runNumber))
        phDict["#RUN_NUMBER#"] = str(runNumber)

        for path in runListener.fileslocations:

            path = self.replaceTagInString(path, phDict)
            filesList = Tools.listFiles(path, runNumber)
            if filesList!=[]:
                return (path, filesList)
        return ('',[])


    def getNewRuns(self):

        tempList = []
        for rl in self.__runListenersList__:
            # get dictionary of run parameters from current run listener
            
            runpList = rl.listen()
            
            for irun, runp in runpList.items():
                runInfo = RunInformation()
                runInfo.runNumber = irun
                runInfo.runListenerName = rl.RunListenerName
                runInfo.runParameters = runp

                rawPath, fileList = self.findRawDataFiles(rl, str(irun))
                runInfo.rawPath = rawPath
                runInfo.nFiles = len(fileList)
                if runp.storedevents<rl.minevents:
                    runInfo.validated = True

                # if no files put it in run DB wiht special status (not NEW) for later check
                #runInfo.rawStatus = NOTRDY
                #else
                #runInfo.rawStatus = OK

                #runInformationList.append(runInfo)
                tempList.append((irun, runInfo))

        runInformationList = []
        for irun, runInfo in sorted(tempList):
            runInformationList.append(runInfo)

        return runInformationList

    def runInfoToDbList(self, runInfoList):
        rs=[]
        rp=[]
        for runInfo in runInfoList:
            rs.append( ( str(runInfo.runNumber), str(runInfo.runListenerName), "NEW", str(runInfo.validated) ) )
            #rs.append( ( str(runInfo.runNumber), str(runInfo.runListenerName), str(runInfo.rawPath), str(runInfo.nFiles), str(runInfo.rawStatus), "NEW", str(runInfo.validated) ) )
            runp = runInfo.runParameters
            rp.append( ( str(runp.run), str(runp.start), str(runp.runtype), str(runp.daqconfig),
                          str(runp.detmask), str(runp.filetag), str(runp.rec),
                          str(runp.datasource), str(runp.stop), str(runp.totaltime),
                          str(runp.cleanstop), str(runp.maxlb), str(runp.partname),
                          str(runp.recevents), str(runp.storedevents), str(runp.l1events),
                          str(runp.l2events), str(runp.efevents), str(runp.errcode),
                          str(runp.tierzerotag) ) )
        return rs, rp

    def listen(self):

        self.logger.debug("listening...")

        # look for new runs
        runInformationList = self.getNewRuns()

        #update DB
        connection = self.getDbConnection()

        # test pour ne pas reinserer les runs deja presents
        #
        cursor = connection.cursor()
        cursor.execute('select run from RUNSTATUS')

        #build a list of runs from Db
        runsFromDb = []
        for row in cursor:
            runsFromDb.append(int(row[0]))

        # only keep runs that are not yet in the Db
        cleanedRunInfoList = []
        for runInfo in runInformationList:
            if int(runInfo.runNumber) not in runsFromDb:
                cleanedRunInfoList.append(runInfo)

        # if news runs, we add them into the Db
        if cleanedRunInfoList!=[]:

            rsList, rpList = self.runInfoToDbList(cleanedRunInfoList)
            #connection.executemany("insert into RUNSTATUS(id, run, listener, rawpath, nfiles, rawstatus, status, validated) values (null, ?, ?, ?, ?, ?, ?)", rsList)
            connection.executemany("insert into RUNSTATUS(id, run, listener, status, validated) values (null, ?, ?, ?, ?)", rsList)
            connection.executemany("insert into RUNPARAMS(id, run, start, runtype, daqconfig, detmask, filetag, rec, datasource, stop, totaltime, cleanstop, maxlb, partname, recevents, storedevents, l1events, l2events, efevents, errcode, tierzerotag) values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rpList)

            #loop on news runs to find where are the datasets and if available
            #ADD rawpath, rawstatus to DB as well

            connection.commit()

            #log new runs
            self.logger.info("new runs found and stored into the Db:")
            for runInfo in cleanedRunInfoList:
                self.logger.info(" * "+str(runInfo))

            # send email !
            subject = "[RunsProvider] INFO: New runs found"
            message = "New runs have been added to the run DB:\n"
            for runInfo in cleanedRunInfoList:
                message = message + " * "+str(runInfo)+"\n"
            self.sendTextMail(subject, message, self.config.MailingList)


        # loop over all runs from DB with rawstatus 'undefined' or not 'OK' or not READY
        # NOTREADY -> files being coopied to castor
        # READY -> files copied, number of files agree to run DB
        # chekc new status adn update

#       else:
#           self.logger.debug("No new valid runs found")

        connection.close()

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
        return


if __name__ == "__main__":
    x=RunsProvider("RunsProviderConfigTest.py")
    x.listen()
