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

# setup globalflags
from AthenaCommon.GlobalFlags  import globalflags
globalflags.ConditionsTag.set_Value_and_Lock("COMCOND-BLKPA-006-05")

# setup lar
from LArConditionsCommon.LArCondFlags import larCondFlags
larCondFlags.useShape = True

# cell reconstruction properties
from CaloRec.CaloCellFlags import jobproperties
jobproperties.CaloCellFlags.doDeadCellCorr = True
jobproperties.CaloCellFlags.doLArCreateMissingCells = False
#JB 20/9/2011
jobproperties.CaloCellFlags.doLArSporadicMasking.set_Value_and_Lock(False)

# tile
from TileRecUtils.TileRecFlags import jobproperties
jobproperties.TileRecFlags.doTileOpt2=True
jobproperties.TileRecFlags.readDigits=True
jobproperties.TileRecFlags.noiseFilter=0
jobproperties.TileRecFlags.TileRunType=8
jobproperties.TileRecFlags.calibrateEnergy=False
jobproperties.TileRecFlags.OfcFromCOOL=False
jobproperties.TileRecFlags.BestPhaseFromCOOL=False
jobproperties.TileRecFlags.correctTime=False
jobproperties.TileRecFlags.correctAmplitude=False

include ("RecExCommon/RecExCommon_topOptions.py")

# use ofc for calib pulses
for i in svcMgr.IOVDbSvc.Folders:
    if i.find('OFC')> 0: svcMgr.IOVDbSvc.Folders.remove(i)
conddb.addFolder("LAR_OFL", '/LAR/ElecCalibOfl/OFC/CaliWaveXtalkCorr')
conddb.addOverride("/LAR/ElecCalibOfl/OFC/CaliWaveXtalkCorr", "LARElecCalibOflOFCCaliWaveXtalkCorr-UPD3-01")
conddb.addOverride("/LAR/ElecCalibOfl/uA2MeV/Symmetry","LARuA2MeV-Rep2011")

# CERN
from glob import glob
catalog_files = glob("/afs/cern.ch/atlas/conditions/poolcond/catalogue/fragments/PoolCat_cond??_data.??????.lar.COND_castor.xml")

svcMgr.PoolSvc.ReadCatalog += ["xmlcatalog_file:%s" % i for i in catalog_files]
# Brum
#svcMgr.PoolSvc.ReadCatalog += ["xmlcatalog_file:/home/atdata5/pjwf/condcalib/PoolFileCatalog.xml"]

#JB 20/9/2011
ToolSvc.LArNoiseMasker.ProblemsToMask= ["deadReadout","deadPhys"]

from TileConditions.TileCondToolConf import *
tileInfoConfigurator.TileCondToolTiming = getTileCondToolTiming( 'COOL','CIS')

tileCondToolOfcCool = getTileCondToolOfcCool('COOL', 'CISPULSE100')
from AthenaCommon.AppMgr import ToolSvc
ToolSvc += tileCondToolOfcCool

from TileConditions.TileConditionsConf import TileCondToolOfc
tileCondToolOfc = TileCondToolOfc()
tileCondToolOfc.TileCondToolPulseShape = getTileCondToolPulseShape('COOL','CISPULSE100')

# turn off masking of bad channels
ToolSvc.TileCellBuilder.maskBadChannels = False
