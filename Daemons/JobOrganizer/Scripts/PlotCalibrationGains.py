#!/bin/env python

#from ROOT import gRandom,TCanvas,TH1F,TH2F
from ROOT import *
import sys
import time

from PyCool import cool
from optparse import OptionParser

from coolTools import *

class L1CaloMap:
 
     def __init__(self,title):
         self.h_1 = TH2F("GainTTsMap" ,title, 50,-25-0.5,24+0.5,64,-0.5,63.5)     
         self.h_2 = TH2F("GainTTsMap2",title, 31,-31.5,30.5,32,-1.,63.)
         self.h_3 = TH2F("GainTTsMap3",title, 64,-32.5,31.5,32,-1.,63.)
         self.h_4 = TH2F("GainTTsMap4",title, 24,-48.5,47.5,16,-1.,63.)
	 
     def Draw(self):
         self.h_4.SetStats(0)	 
         self.h_3.SetStats(0)
         self.h_2.SetStats(0)
         self.h_1.SetStats(0)

         self.h_4.Draw("colz")	 
         self.h_3.Draw("colz same")
         self.h_2.Draw("colz same")
         self.h_1.Draw("colz same")
	 
     def Fill(self,eta,phi,gain=1):
         if eta>= -25 and eta <= 24:
              self.h_1.Fill(eta,phi,gain)
         elif eta >= -31 and eta <= 29:
              self.h_2.Fill(eta,phi,gain)
         elif eta >= -32 and eta <= 31:
              self.h_3.Fill(eta,phi,gain)
         elif eta >= -49 and eta <= 44:
              self.h_4.Fill(eta+1,phi,gain)
         else:
              print " Take it easy, such eta doesn't exist!"
	      
     def SetMinimum(self,minimum):
         self.h_4.SetMinimum(minimum)	 
         self.h_3.SetMinimum(minimum)
         self.h_2.SetMinimum(minimum)
         self.h_1.SetMinimum(minimum)
     	                          
     def SetMaximum(self,maximum):
         self.h_4.SetMaximum(maximum)	 
         self.h_3.SetMaximum(maximum)
         self.h_2.SetMaximum(maximum)
         self.h_1.SetMaximum(maximum)


class L1CaloGeometryConvertor:

     def __init__(self):
          input = open('/afs/cern.ch/user/l/l1ccalib/jb/COOLIdDump.txt')

          self.list_of_channels_em={}
          self.list_of_channels_had={}

          for line in input.readlines():
               parts = line.split(' ')
               emCool = parts[4].rstrip()
               hadCool = parts[5].rstrip()
               self.list_of_channels_em[(parts[0],parts[1])]  = '0x'+emCool
               self.list_of_channels_had[(parts[0],parts[1])] = '0x'+hadCool
     
          input.close()
	  
     def LoadReceiverPPMMap(self):
     
         self.receiver_to_ppm_map={}
         self.UNIX2COOL = 1000000000
	 
         # get database service and open database
         dbSvc = cool.DatabaseSvcFactory.databaseService()

         dbString = 'oracle://ATLAS_COOLPROD;schema=ATLAS_COOLONL_TRIGGER;dbname=COMP200'
         try:
           db = dbSvc.openDatabase(dbString, False)        
         except Exception, e:
           print 'Error: Problem opening database', e
           sys.exit(1)

         folder_name = "/TRIGGER/Receivers/RxPpmIdMap"
         folder=db.getFolder(folder_name)
         ch = folder.listChannels()
       
         startUtime = int(time.time())
         endUtime = int(time.time())
         startValKey = startUtime * self.UNIX2COOL
         endValKey = endUtime * self.UNIX2COOL
         chsel = cool.ChannelSelection(0,sys.maxint)

         try:
           itr=folder.browseObjects(startValKey, endValKey, chsel)
         except Exception, e:
           print e
           sys.exit(1)

         for row in itr:
           ReceiverId = hex(int(row.channelId()))
           payload = row.payload()
           PPMId = hex(int(payload['ppmid']))
           self.receiver_to_ppm_map[ReceiverId]= PPMId
  
#         print self.receiver_to_ppm_map
         # close database
         db.closeDatabase()


     def getPPMfromReceiver(self,ReceiverId):
     
       if self.receiver_to_ppm_map.has_key(ReceiverId):
         return self.receiver_to_ppm_map[ReceiverId]
       else:
         return ''	 

     def getReceiverfromPPM(self,PPMId):
        
       ReceiverChannels = [item[0] for item in self.receiver_to_ppm_map.items() if item[1]==PPMId]       
       return ReceiverChannels
	 

     def getCoolEm(self,eta,phi):
          if self.list_of_channels_em.has_key((str(i_eta),str(i_phi))) == True:
              cool = self.list_of_channels_em[(str(i_eta),str(i_phi))]
              cool.rstrip()
              cool.lstrip()
              return (cool)
          else:
              return ('')         
     
     
     def getCoolHad(self,eta,phi):
          if self.list_of_channels_had.has_key((str(i_eta),str(i_phi))) == True:
              cool = self.list_of_channels_had[(str(i_eta),str(i_phi))]
              cool.rstrip()
              cool.lstrip()
              return (cool)
          else:
              return ('')         
     
     def isCoolEm(self,CoolId):
          return (CoolId in self.list_of_channels_em.values())
	  
     def isCoolHad(self,CoolId):
          return (CoolId in self.list_of_channels_had.values())
	  	
     def getEtaBin(self,CoolId):
          if self.isCoolEm(CoolId):
            channel = [item[0] for item in self.list_of_channels_em.items() if item[1]==CoolId]
            return int(channel[0][0])
          elif self.isCoolHad(CoolId):
            channel = [item[0] for item in self.list_of_channels_had.items() if item[1]==CoolId]
            return int(channel[0][0])
          else:
            return -1
	  
     def getPhiBin(self,CoolId):
          if self.isCoolEm(CoolId):
            channel = [item[0] for item in self.list_of_channels_em.items() if item[1]==CoolId]
            return int(channel[0][1])
          elif self.isCoolHad(CoolId):
            channel = [item[0] for item in self.list_of_channels_had.items() if item[1]==CoolId]
            return int(channel[0][1])
          else:
            return -1

class GainReader:	  

     def __init__(self):	  	  	  

          self.measured_gains={}
          self.reference_gains={}
          self.UNIX2COOL = 1000000000

     def LoadGainsXml(self,name):
     
          input_file = open(name)

          for line in input_file.readlines():
            parts = line.split(' ')
            if parts[0] == '<Channel':
              list_cool=parts[1].split('\'')
              cool_id=list_cool[1]
              list_gain=parts[2].split('\'')
              gain=list_gain[1]
              self.measured_gains[cool_id]=gain

          input_file.close()

     def LoadReferenceXml(self,name): 

          input_gains_reference = open(name)

          for line in input_gains_reference.readlines():
            parts = line.split(' ')
            if parts[0] == '<Channel':
              list_cool=parts[1].split('\'')
              cool_id=list_cool[1]
              list_gain=parts[2].split('\'')
              gain=list_gain[1]
              self.reference_gains[cool_id]=gain

     def LoadGainsSqlite(self,name):

       # get database service and open database
       dbSvc = cool.DatabaseSvcFactory.databaseService()

       dbString='sqlite://;schema='+name+';dbname=L1CALO'
       try:
         db = dbSvc.openDatabase(dbString, False)        
       except Exception, e:
         print 'Error: Problem opening database', e
         sys.exit(1)

       folder_name = '/TRIGGER/L1Calo/V1/Results/EnergyScanResults'
       folder=db.getFolder(folder_name)
       ch = folder.listChannels()
       
       startUtime = int(time.time())
       endUtime = int(time.time())
       startValKey = startUtime * self.UNIX2COOL
       endValKey = endUtime * self.UNIX2COOL
       chsel = cool.ChannelSelection(0,sys.maxint)

       try:
         itr=folder.browseObjects(startValKey, endValKey, chsel)
       except Exception, e:
         print e
         sys.exit(1)

       for row in itr:
         CoolId = hex(int(row.channelId()))
         payload = row.payload()
         self.measured_gains[CoolId]=payload['Slope']
  
#       print self.measured_gains
       # close database
       db.closeDatabase()

     def LoadReferenceSqlite(self,name):

       # get database service and open database
       dbSvc = cool.DatabaseSvcFactory.databaseService()

       dbString='sqlite://;schema='+name+';dbname=L1CALO'
       try:
         db = dbSvc.openDatabase(dbString, False)        
       except Exception, e:
         print 'Error: Problem opening database', e
         sys.exit(1)

       folder_name = '/TRIGGER/L1Calo/V1/Results/EnergyScanResults'
       folder=db.getFolder(folder_name)
       ch = folder.listChannels()
       
       startUtime = int(time.time())
       endUtime = int(time.time())
       startValKey = startUtime * self.UNIX2COOL
       endValKey = endUtime * self.UNIX2COOL
       chsel = cool.ChannelSelection(0,sys.maxint)

       try:
         itr=folder.browseObjects(startValKey, endValKey, chsel)
       except Exception, e:
         print e
         sys.exit(1)

       for row in itr:
         CoolId = hex(int(row.channelId()))
         payload = row.payload()
         self.reference_gains[CoolId]=payload['Slope']
  
#       print self.measured_gains
       # close database
       db.closeDatabase()


     def LoadReferenceOracle(self,mapping_tool,flag='loweta'):

       # get database service and open database
       dbSvc = cool.DatabaseSvcFactory.databaseService()

       dbString = 'oracle://ATLAS_COOLPROD;schema=ATLAS_COOLONL_TRIGGER;dbname=COMP200'
       try:
         db = dbSvc.openDatabase(dbString, False)        
       except Exception, e:
         print 'Error: Problem opening database', e
         sys.exit(1)

       folder_name = "/TRIGGER/Receivers/Factors/CalibGains"
       folder=db.getFolder(folder_name)
       ch = folder.listChannels()
       
       startUtime = int(time.time())
       endUtime = int(time.time())
       startValKey = startUtime * self.UNIX2COOL
       endValKey = endUtime * self.UNIX2COOL
       chsel = cool.ChannelSelection(0,sys.maxint)

       try:
         itr=folder.browseObjects(startValKey, endValKey, chsel)
       except Exception, e:
         print e
         sys.exit(1)

       for row in itr:
         ReceiverId = hex(int(row.channelId()))
         PPMId = mapping_tool.getPPMfromReceiver(ReceiverId)
         payload = row.payload()
         gain = payload['factor']
 # JB : here I need to do something for double gain channels!	for these channels there are more then
 #      one receiver channels available, one of them should be picked depending on the value
 #      of chsel flag 

#         print  "ReceiverId=", ReceiverId," PPM Id=",  PPMId, "getReceiverfromPPM()=",mapping_tool.getReceiverfromPPM(PPMId)
#	 print "  gain = " , gain
         self.reference_gains[PPMId]=gain
  
 #      print self.reference_gains
       # close database
       db.closeDatabase()


     def getGain(self,coolId):
           if (coolId in self.measured_gains):
             return float(self.measured_gains[coolId])
           else:
             return ''

     def getReferenceGain(self,coolId):
           if (coolId in self.reference_gains):
             return float(self.reference_gains[coolId])
           else:
             return ''  


class EmPartitionPlots:
  
     def __init__(self,name,nbins=40,minimum=0.,maximum=2.):
     
       self.nPartitions=5
       self.ext  = ["all","00_15","15_25","25_32","32_50"]
       self.name = ["all","EMB","EMEC outer","EMEC Inner","FCAL 1"]


       self.his_partitions  = []

       for i_em_partition in range(0,self.nPartitions):
         self.his_partitions.append(TH1F("GainTTEm"+self.ext[i_em_partition],name+" for "+self.name[i_em_partition],nbins,minimum,maximum))

     def get_partition_number(self,eta_bin):

       indem = -1
       if ( -9 <= eta_bin and eta_bin <= 8):                      
            indem = 1
       elif ((eta_bin>8 and eta_bin<=14) or (eta_bin>=-15 and eta_bin<-9)):  
#       elif ((eta_bin>8 and eta_bin<14)  or (eta_bin>-15 and eta_bin<-9)):     # cut out overlap
            indem = 1
       elif ((eta_bin>14 and eta_bin<=24) or (eta_bin>=-25 and eta_bin<-15)):
            indem = 2
       elif ((eta_bin>24 and eta_bin<=31) or (eta_bin>=-32 and eta_bin<-25)): 
            indem = 3
       elif ((eta_bin>31)          or  (eta_bin<-32)):           
            indem = 4

       return indem


     def Fill(self,eta_bin,gain):
     
        partition=self.get_partition_number(eta_bin)
	
        if partition > 0:
          self.his_partitions[0].Fill(gain)
          self.his_partitions[partition].Fill(gain)
        else:
          print "Warning in EmPartitionPlots, nonexisting partition!"  
	  

class HadPartitionPlots:
  
     def __init__(self,name,nbins=40,minimum=0.,maximum=2.):
     
       self.nPartitions=6
       self.ext = ["all","00_09","09_15","15_25","25_32","32_50"]
       self.name = ["all","Tile LB","Tile EB","HEC outer", "HEC inner","FCAL 2/3"]
       
       self.his_partitions  = []

       for i_had_partition in range(0,self.nPartitions):
         self.his_partitions.append(TH1F("GainTTHad"+self.ext[i_had_partition],name+" for "+self.name[i_had_partition],nbins,minimum,maximum))
       

     def get_partition_number(self,eta_bin):

       indhad = -1
       if ( -9 <= eta_bin and eta_bin <= 8):                      
            indhad = 1
       elif ((eta_bin>8 and eta_bin<=14)  or (eta_bin>=-15 and eta_bin<-9)):
#       elif ((eta_bin>8 and eta_bin<14)  or (eta_bin>-15 and eta_bin<-9)):    # cut out overlap  
            indhad = 2
       elif ((eta_bin>14 and eta_bin<=24) or (eta_bin>=-25 and eta_bin<-15)): 
            indhad = 3
       elif ((eta_bin>24 and eta_bin<=31) or (eta_bin>=-32 and eta_bin<-25)): 
            indhad = 4
       elif ((eta_bin>31)          or (eta_bin<-32)):           
            indhad = 5

       return indhad     
     
     
     
     def Fill(self,eta_bin,gain):
     
        partition=self.get_partition_number(eta_bin)
	
        if partition > 0:
          self.his_partitions[0].Fill(gain)
          self.his_partitions[partition].Fill(gain)
        else:
          print "Warning in HadPartitionPlots, nonexisting partition!"  

if __name__ == "__main__":

  print "Starting plot_gains_xml"

  parser = OptionParser()
  
  parser.add_option("-f","--InputFile",action="store",type="string",dest="input_file_name",help="Name of input file")

  parser.add_option("-r","--ReferenceFile",action="store",type="string",dest="reference_file_name",help="Name of reference file")

  parser.add_option("--InputXml",action="store_true",dest="isInputXml",help="Input is .xml file")
  parser.add_option("--InputSqlite",action="store_true",dest="isInputSqlite",help="Input is .sqlite file")
  parser.add_option("--RefXml",action="store_true",dest="isRefXml",help="Reference is .xml file")
  parser.add_option("--RefSqlite",action="store_true",dest="isRefSqlite",help="Reference is .sqlite file")
  parser.add_option("--RefOracle",action="store_true",dest="isRefOracle",help="Reference is from Oracle")
   
  (options, args) = parser.parse_args()
  
  gStyle.SetPalette(1)
  gStyle.SetOptStat(111111)
  c1 = TCanvas('c1','Example',200,10,700,500)

  h_gains_em  = L1CaloMap("Eta-phi map of EM gains")
  h_gains_had = L1CaloMap("Eta-phi map of HAD gains")

  h_unfitted_em  = L1CaloMap("Eta-phi map of EM failed fits")
  h_unfitted_had = L1CaloMap("Eta-phi map of HAD failed fits")

  h_gains_em_reference  = L1CaloMap("Eta-phi map of EM gains (gain-reference)")
  h_gains_had_reference = L1CaloMap("Eta-phi map of HAD gains (gain-reference)")

  em_partition_gains = EmPartitionPlots(" EM gains",40,0.6,1.4)
  had_partition_gains = HadPartitionPlots(" HAD gains",40,0.5,2.5)

  em_partition_gains_ref = EmPartitionPlots(" EM gains - reference",40,-0.2,0.2)
  had_partition_gains_ref = HadPartitionPlots(" HAD gains - reference",40,-1.,1.)


  geometry_convertor = L1CaloGeometryConvertor()
  receiver_gains     = GainReader()

  if options.isInputXml == True:
    print "Taking input from xml file: ", options.input_file_name
    receiver_gains.LoadGainsXml(options.input_file_name)
  elif options.isInputSqlite == True:
    print "Taking input from Sqlite file: ", options.input_file_name
    receiver_gains.LoadGainsSqlite(options.input_file_name)
  else:
    print "No option for input file selected, assuming sqlite file energyscanresults.sqlite"
    receiver_gains.LoadGainsSqlite("energyscanresults.sqlite")
         

  if options.isRefXml == True:
    print "Taking reference from Xml file: ",options.reference_file_name
    receiver_gains.LoadReferenceXml(options.reference_file_name)
  elif options.isRefSqlite == True:
    print "Taking reference from Sqlite file: ",options.reference_file_name
    receiver_gains.LoadReferenceSqlite(options.reference_file_name)
  elif options.isRefOracle == True:
    print "Taking reference from Oracle"
    geometry_convertor.LoadReceiverPPMMap()
    receiver_gains.LoadReferenceOracle(geometry_convertor)
  else:
    print " No option for reference file, assuming Oracle"
    geometry_convertor.LoadReceiverPPMMap()
    receiver_gains.LoadReferenceOracle(geometry_convertor)
          
      
  for i_eta in range(-49,45):
     for i_phi in range(0,64):
     
       coolEm  = geometry_convertor.getCoolEm(i_eta,i_phi)
       coolHad = geometry_convertor.getCoolHad(i_eta,i_phi)
       
       if not coolEm == '':                           # there is a channel for this eta-phi
       
         gain = receiver_gains.getGain(coolEm)
         reference_gain = receiver_gains.getReferenceGain(coolEm)

         if (not gain == '') and (not reference_gain == ''):        # both  gains should be available
	 
           em_partition_gains.Fill(i_eta,gain)           
           h_gains_em.Fill(i_eta,i_phi,gain)
           if gain == -1. :
             h_unfitted_em.Fill(i_eta,i_phi)  
           else:
             em_partition_gains_ref.Fill(i_eta,gain-reference_gain)  
             h_gains_em_reference.Fill(i_eta,i_phi,gain-reference_gain)

       if not coolHad == '':                         # there is a channel for this eta-phi

         gain = receiver_gains.getGain(coolHad)
         reference_gain = receiver_gains.getReferenceGain(coolHad)

         if (not gain == '') and (not reference_gain == ''):       # both gains should be available

           had_partition_gains.Fill(i_eta,gain)
           h_gains_had.Fill(i_eta,i_phi,gain)
           if gain == -1. :
             h_unfitted_had.Fill(i_eta,i_phi)  
           else:
             had_partition_gains_ref.Fill(i_eta,gain-reference_gain)
             h_gains_had_reference.Fill(i_eta,i_phi,gain-reference_gain)
	    

	   
#print measured_gains	 
  c1.cd()
  h_gains_em.SetMinimum(0.8)
  h_gains_em.SetMaximum(1.2)
  h_gains_em.Draw()
  c1.Print("Gains.ps(")

  h_gains_had.SetMinimum(0.6)
  h_gains_had.SetMaximum(1.4)
  h_gains_had.Draw()
  c1.Print("Gains.ps")

  c1.cd()
  gPad.SetLogy(0)

  h_gains_em_reference.SetMinimum(-0.5)
  h_gains_em_reference.SetMaximum(0.5)
  h_gains_em_reference.Draw()
  c1.Print("Gains.ps")

  h_gains_had_reference.SetMinimum(-0.5)
  h_gains_had_reference.SetMaximum(0.5)
  h_gains_had_reference.Draw()
  c1.Print("Gains.ps")


  c1.cd()
  for i_p in range(0,em_partition_gains.nPartitions):
    if em_partition_gains.his_partitions[i_p].GetEntries() > 0:
      gPad.SetLogy()
    else:
      gPad.SetLogy(0)
    em_partition_gains.his_partitions[i_p].Draw()
    c1.Print("Gains.ps")
  
  c1.cd()
  for i_p in range(0,had_partition_gains.nPartitions):
    if had_partition_gains.his_partitions[i_p].GetEntries() > 0:
      gPad.SetLogy()
    else:
      gPad.SetLogy(0)
    had_partition_gains.his_partitions[i_p].Draw()
    c1.Print("Gains.ps")
  
  
  c1.cd()
  for i_p in range(0,em_partition_gains_ref.nPartitions):
    if em_partition_gains_ref.his_partitions[i_p].GetEntries() > 0:
      gPad.SetLogy()
    else:
      gPad.SetLogy(0)
    em_partition_gains_ref.his_partitions[i_p].Draw()
    c1.Print("Gains.ps")
  
  c1.cd()
  for i_p in range(0,had_partition_gains_ref.nPartitions):
    if had_partition_gains_ref.his_partitions[i_p].GetEntries() > 0:
      gPad.SetLogy()
    else:
      gPad.SetLogy(0)
    had_partition_gains_ref.his_partitions[i_p].Draw()
    c1.Print("Gains.ps")

  c1.cd()
  gPad.SetLogy(0)

  h_unfitted_em.Draw()
  c1.Print("Gains.ps")

  h_unfitted_had.Draw()
  c1.Print("Gains.ps)")

  print "finished!"
