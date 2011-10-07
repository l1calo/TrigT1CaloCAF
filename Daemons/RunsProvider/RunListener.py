#!/usr/bin/env python

import sys, getopt, time, os
import logging
from CoolConvUtilities import AtlCoolLib
#from CoolConvUtilities.RunLister import coolRunLister
from RunLister import coolRunLister
from CoolConvUtilities.RunLister import timeRep, boolRep, noneZero, noneStr

#______________________________________________________________________
def coolTimeFromRunLumi(runNum, lbkNum):
    """
    Returns COOL timeStamp build from run and lumi block numbers
    """
    return (int(runNum)<<32) + int(lbkNum)

#
#______________________________________________________________________
def decodeTimeString(timeString):
    """
    Retruns UNIX time stamp given an input time string
    """
    return int(time.mktime(time.strptime(timeString,"%Y-%m-%d %H:%M:%S")))


class RunListener:
    def __init__(self, name):

        self.RunListenerName=name

        self.logger = None

        # defaults for optional parameters

        #connection parameters
        self.tdaqdbname='COOLONL_TDAQ/COMP200'
        self.trigdbname='COOLONL_TRIGGER/COMP200'
        self.statusdbname='COOLOFL_GLOBAL/COMP200'
        self.loglevel=2
        self.oracle=False

        # filtering parameters
        self.reconly=False
        self.detmask=0
        self.runtype=""
        self.tag=""
        self.detstatus=""
        self.detstatustag="HEAD"
        self.daqpartition = []
        self.tierzerotag = []
        self.NOTtierzerotag = []
        self.gainstrategy = []

        self.format="acert"
        self.reverse=False

        self.stoptimestamp = None
        self.cleanstop = None
        self.hasevents = None
        self.minevents = 0

        self.runlisttool = None

        self.RUNMAX=0x7FFFFFFF

        self.runMap = {}
        self.lastKnownRun = 0

        self.initialRun = 0
        self.fileslocations = []

        self.initLogging(self.RunListenerName)
        self.logger.info("========================================")
        self.logger.info("RunListener in init")

        self.logger.info("RunListener initialized")
        self.logger.info("========================================")


    def dumpConfig(self):
        
        text = '\n'+ \
            "RunListener "+ self.RunListenerName + "initialised with the following parameters:\n" + \
            "TDAQ DB: " + self.tdaqdbname + '\n' + \
            "TRIG DB: " + self.trigdbname + '\n' + \
            "Status DB: " + self.tdaqdbname + '\n' + \
            "log level: " + str(self.loglevel) + '\n' + \
            "oracle: " + str(self.oracle) + '\n' + \
            "rec. only: " + str(self.reconly) + '\n' + \
            "det. mask: " + str(self.detmask) + '\n' + \
            "run type: " + self.runtype + '\n' + \
            "det. status: " + self.detstatus + '\n' + \
            "det. status tag: " + self.detstatustag + '\n'+ \
            "daq partition: \n"
            
        for part in self.daqpartition:
            text = text + ' * '+ part + '\n'
        text = text + "tierzerotag: \n"
        for part in self.tierzerotag:
            text = text + ' * '+ part + '\n'
        text = text + "NOTtierzerotag: \n"
        for part in self.NOTtierzerotag:
            text = text + ' * '+ part + '\n'
        text = text + "gainstrategy: \n"
        for part in self.gainstrategy:
            text = text + ' * '+ part + '\n'
            
        text = text +  \
            "tag: " + self.tag + '\n' + \
            "format: " + self.format + '\n' + \
            "reverse: " + str(self.reverse) + '\n' + \
            "stoptimestamp: " + str(self.stoptimestamp) + '\n' + \
            "cleanstop: " + str(self.cleanstop) + '\n' + \
            "hasevents: " + str(self.hasevents) + '\n' + \
            "minevents: " + str(self.minevents) + '\n' + \
            "last valid run known: " + str(self.lastKnownRun) + '\n'
            #"files locations: " + self.fileslocations + '\n'
            
        self.logger.info(text)

    def maxRunIndex(self, runmap):
        maxRunIndex=0
        for irun in runmap.iterkeys():
            if  irun>maxRunIndex: maxRunIndex = irun
        return maxRunIndex

    def initRunListener(self):
        self.logger.info("===> from initRunListener <===")
        self.dumpConfig()
        self.runlisttool = coolRunLister(self.tdaqdbname,self.trigdbname,self.statusdbname,self.oracle,self.loglevel)
        self.runlisttool.setSelection(self.reconly,self.detmask,self.runtype,self.tag,self.detstatus,self.detstatustag)

        if self.initialRun==0:

            nhours = 6
            tsnow = int(time.time())*1000000000L
            tsmin = tsnow - nhours * 3600 * 1000000000L

            self.runlisttool.listFromTime(tsmin,tsnow)

            self.logger.debug("looking for runs between now:" + str(tsnow)+" and " + str(nhours)+ " hours ago: "+ str(tsmin) )
            rawRunList = self.runlisttool.runmap

            cleanedRunList = self.filterRuns(rawRunList)

            self.lastKnownRun = self.maxRunIndex(cleanedRunList)
            self.logger.debug("last valid run found: " + str(self.lastKnownRun))
            self.logger.debug('\n'+self.runToStr(cleanedRunList[self.lastKnownRun ],self.format))
            
            #self.lastKnownRun = 92200

            self.runlisttool.close()

        else:
            self.lastKnownRun = self.initialRun

        return

    def listen(self):
        self.logger.info("===> listening for new valid runs <===")

        # look for new runs after last one
        #print self.lastKnownRun, self.RUNMAX

        self.logger.debug("initialising coolRunLister")
        self.runlisttool = coolRunLister(self.tdaqdbname,self.trigdbname,self.statusdbname,self.oracle,self.loglevel)

        self.logger.debug("applying selections to coolRunLister")

        # The 'reconly' parameter is set to False below in setSelection(), because it is not handled correctly.
        # Setting it to True returns only the runs with rec==True, but there is an inversion in the run DB:
        # runs with rec==1 (True) are not recorded, while runs with rec==0 (False) are
        # the recorded/notrecorded is done later in isValidRun() depending on self.reconly

        #self.runlisttool.setSelection(self.reconly,self.detmask,self.runtype,self.tag,self.detstatus,self.detstatustag)
        self.runlisttool.setSelection(False,self.detmask,self.runtype,self.tag,self.detstatus,self.detstatustag)

        self.logger.info("last valid run: "+ str(self.lastKnownRun) )
        self.logger.info("searching for new runs from "+ str(self.lastKnownRun+1) + " to " + str(self.RUNMAX))
        #self.runlisttool.listFromRuns(self.lastKnownRun+1, self.RUNMAX)
        self.runlisttool.listFromRuns(self.lastKnownRun+1, 1000000000)

        rawRunList = self.runlisttool.runmap

        self.runlisttool.close()

        cleanedRunList = self.filterRuns(rawRunList)

        if cleanedRunList!={}:
            self.lastKnownRun = self.maxRunIndex(cleanedRunList)
            self.logger.debug("new last known run: "+ str(self.lastKnownRun))
            self.logger.debug('\n'+self.runListToStr(cleanedRunList,"acertd"))
        else:
            self.logger.debug(" No new valid run. Last known valid run still: "+ str(self.lastKnownRun))

        return cleanedRunList

#       self.runMap = cleanedRunList

#       print self.runMap
##      return False
        # return True si runMap not empty
        # set new lat runs
#       if self.runMap!=None:
#           if len(self.runMap)!=0:
#               self.lastKnownRun = self.maxRunIndex(self.runMap)
#               self.logger.info(" *** new valid runs found. New last valid run: "+ str(self.lastKnownRun) )
#               return True
#           else:
#               self.logger.info(" no new valid runs found.")
#               return False
#       self.logger.error("self.runMap not defined - Should not happen")
#       return False

    def listNewRuns(self):
        return sorted(self.runMap.iterkeys())

    def runListToStr(self, runList, format=""):
        tmp=""
        for irun, runp in sorted(runList.items()):
            tmp=tmp+self.runToStr(runp, format)
        return tmp

#   def runToStr(self, runp):
#       return self.runToStr(runp, self.format)

    def runToStr(self, runp, format=""):
        title="     Run   Events  LumiB"
        if ('t' in format):
            title+='            StartTime             StopTime'
        if ('a' in format):
            title+=' L1Events L2Events EFEvents'
        if ('e' in format):
            title+=' ErrC'
        if ('r' in format):
            title+=' Rec Cln'
        if ('c' in format):
            title+=' RunType                  DetectorMask'
        if ('d' in format):
            title+=' DAQConfiguration     PartitionName      FilenameTag          tierZeroTag         GainStrategy'
        #print title

#       runp=self.runMap[irun]
        line="%8i %8i %6i" % (runp.run,noneZero(runp.storedevents),noneZero(runp.maxlb))
        if ('t' in format):
            line+=' %20s %20s' % (timeRep(runp.start),timeRep(runp.stop))
        if ('a' in format):
            line+=' %8i %8i %8i' % (noneZero(runp.l1events),noneZero(runp.l2events),noneZero(runp.efevents))
        if ('e' in format):
            line+=' %4i' % runp.errcode
        if ('r' in format):
            line+=' %3s %3s' % (boolRep(runp.rec),boolRep(runp.cleanstop))
        if ('c' in format):
            line+=' %-20s %16x' % (runp.runtype,runp.detmask)
        if ('d' in format):
            line+=' %-20s %-16s %-20s %-20s %-20s' % (runp.daqconfig,noneStr(runp.partname),runp.filetag,runp.tierzerotag,runp.gainstrategy)
        #print line
        return title + '\n' + line + '\n'


    def initLogging(self, name):
        #create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        #create file handler and set level to debug
        logdir = os.environ['PWD']+'/logs/'
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        fh = logging.FileHandler(logdir+'/'+'RunListener_'+name+'_'+ time.strftime('%Y%m%d_%H%M')+'.log','w')
        fh.setLevel(logging.DEBUG)

        #create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s", datefmt='%Y-%m-%d %H:%M')

        #add formatter to fh
        fh.setFormatter(formatter)

        #add ch to logger
        self.logger.addHandler(fh)

    def filterRuns(self, rawRunList):
        #iter over timer in rawrunlist

        cleanedRuns = {}

        for irun, runp in rawRunList.items():

            # check if valid run
            if self.isValidRun(runp):
                #add to output dictionnary if ok
                cleanedRuns[irun] = runp

        return cleanedRuns

    def isValidRun(self, runp):
        bIsValidRun = True

#       runp.storedevents
#       runp.maxlb
#       runp.errcode

        if self.hasevents==True:
            if runp.l1events==0 and runp.l2events==0 and runp.efevents==0 and runp.storedevents==0: return False

        if self.stoptimestamp==True:
            if timeRep(runp.stop)=='unknown': return False

        if self.cleanstop==True:
            if not runp.cleanstop: return False

#        if self.daqpartition!="":
#            if runp.partname!=self.daqpartition: return False

        if self.daqpartition!=[]:
            if runp.partname not in self.daqpartition: return False

        if self.tierzerotag!=[]:
            if runp.tierzerotag not in self.tierzerotag: return False

        if self.NOTtierzerotag!=[]:
            if runp.tierzerotag in self.NOTtierzerotag: return False

        if self.gainstrategy!=[]:
            if runp.gainstrategy not in self.gainstrategy: return False

        if self.reconly==True:
            # the logic is inversed so far: True -> not recorded / False->recorded
            # so we only keep the runs with runp.rec==False when reconly is set to True
            if runp.rec==True: return False

        return bIsValidRun

