# $Id$

###################################################################3
# Define the input file here.
#

from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
#RAW_DATA_SETS#
athenaCommonFlags.FilesInput.set_Value_and_Lock(athenaCommonFlags.BSRDOInput())
#athenaCommonFlags.FilesInput = [ "/tmp/morrisj/lar/data11_calib.00178063.calibration_L1CaloEnergyScan.daq.RAW._lb0000._SFI-LVL1-1._0001.data" ]

###################################################################3
# Define the output file here.
#

if not globals().get('tupleFileOutput'):
    tupleFileOutput = 'L1CaloCalibD3PD.root'

from D3PDMakerConfig.D3PDProdFlags import prodFlags
prodFlags.WriteL1CALOD3PD = True
prodFlags.WriteL1CALOD3PD.FileName = tupleFileOutput
prodFlags.WriteL1CALOD3PD.lock()

###################################################################3
# Define other job options here.
#

athenaCommonFlags.EvtMax = -1

####################################################################
# Configure RecExCommon.
#

from RecExConfig.RecFlags import rec
rec.DPDMakerScripts.append( "L1CaloD3PDMaker/L1CaloD3PD_RAW_prodJobOFragment.py" )
rec.doCalo.set_Value_and_Lock( True )
rec.Commissioning.set_Value_and_Lock(True)
# temporary fix for data12
#rec.projectName.set_Value_and_Lock("data11_calib")

# needed for 17.2.0.2
from CaloRec.CaloCellFlags import jobproperties
jobproperties.CaloCellFlags.doPileupOffsetBCIDCorr = False

disableRecJobOpts = ('doAOD', 'doAODCaloCells', 'doAODall', 'doAlfa', 'doApplyAODFix', 'doCBNT', 'doCheckDictionary',
                    'doCheckJOT',  'doDetStatus', 'doDetailedAuditor', 'doDetailedPerfMon', 'doDumpMC',
                    'doDumpPoolInputContent', 'doDumpProperties', 'doDumpTDS', 'doDumpTES', 'doESD', 'doEdmMonitor',
                    'doEgamma', 'doFileMetaData', 'doFloatingPointException', 'doForwardDet', 'doHeavyIon', 'doHist',
                    'doJetMissingETTag', 'doJiveXML', 'doLowPt', 'doLucid', 'doMinimalRec', 'doMonitoring',
                    'doMuonCombined', 'doNameAuditor', 'doPerfMon', 'doPersint', 'doPyDump', 'doRestrictedESD', 'doSGAuditor',
                    'readAOD', 'readESD', 'readTAG','doWriteAOD','doTruth','doTagRawSummary','doWriteTAG')

for p in disableRecJobOpts:
   getattr(rec, p).set_Value_and_Lock(False)

#for i in dir(rec):
  #try:
    #print getattr(rec,i)
  #except ValueError:
    #pass

include ("RecExCommon/RecExCommon_topOptions.py")
