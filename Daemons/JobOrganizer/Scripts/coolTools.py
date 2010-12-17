#!/bin/env python
import sys


def getFolderPath(folder):
    resultFolders = [ "PprDacScanResults", "PprPedestalRunResults", 
                      "PprReadoutScanResults", "PprPhos4ScanResults" ]

    validFolders = [ "PprChanCalib", "PpmDeadChannels" ]

    l1caloString = "/TRIGGER/L1Calo/"


    if folder in resultFolders:
        return l1caloString+"Results"
    elif folder in validFolders:
        return l1caloString+"Calibration"
    else:
        print "Error: Folder ",folder," not supported"
        sys.exit(1)



def getFolderPathNew(version,prefix,folder):
    resultFolders = [ "PprDacScanResults", "PprPedestalRunResults", 
                      "PprReadoutScanResults", "PprPhos4ScanResults" ]

    validFolders = [ "PprChanCalib" ]

    calibFolders = [ "PpmDeadChannels" ]

    l1caloString = "/TRIGGER/L1Calo/"+version+"/"

    if folder in resultFolders:
        return l1caloString+"Results"+"/"+prefix
    elif folder in validFolders:
        return l1caloString+"Calibration"+"/"+prefix
    elif folder in calibFolders:
        return l1caloString+"Calibration"        
    else:
        print "Error: Folder ",folder," not supported"
        sys.exit(1)
        


class CoolChannelIdDecoder:
    
    def crate(self, coolChannelId):
        return (coolChannelId & 0xff000000) >> 24
    
    def module_type(self, coolChannelId):
        return (coolChannelId & 0x00f00000) >> 20;
    
    def module(self, coolChannelId):
        return (coolChannelId & 0x000f0000) >> 16
    
    def slot(self, coolChannelId):
        module = self.module(coolChannelId)
        module_type = self.module_type(coolChannelId)
        
        if module_type==1: return module+5 #PPM
        if module_type==2: return module+5 #CPM
        if module_type==3: return module+4 #JEM

    def submodule(self, coolChannelId):
        return (coolChannelId & 0x0000ff00) >> 8

    def channel(self, coolChannelId):
        return (coolChannelId & 0x000000ff) >> 0

    def toString(self, coolChannelId):
        crate = str(self.crate(coolChannelId))
        module = str(self.module(coolChannelId))
        submodule= str(self.submodule(coolChannelId))
        channel = str(self.channel(coolChannelId))
        return 'crate: ' + crate + ' module: ' +  module + ' submodule: '+ submodule +' channel: '+ channel

    def getName(self, coolChannelId):
        crate     = self.crate(coolChannelId)
        module    = self.module(coolChannelId)
        submodule = self.submodule(coolChannelId)
        channel   = self.channel(coolChannelId)
        return "pp%2.2d"%crate + "-ppm%2.2d"%module + "-mcm%2.2d"%submodule + "-chn%1.1d"%channel

    def isValid(self, coolChannelId):
        crate     = self.crate(coolChannelId)
        module    = self.module(coolChannelId)
		
        if   (crate == 2):
            if   (module == 0): return False
            elif (module == 8): return False
            else:               return True
        elif (crate == 3):
            if   (module == 0): return False
            elif (module == 8): return False
            else:               return True
        else: return True

