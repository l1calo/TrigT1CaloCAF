################################################################################
# config
################################################################################

#EvtMax = -1
EvtMax = 1
SkipEvents = 0

from AthenaCommon.AthenaCommonFlags  import athenaCommonFlags
#RAW_DATA_SETS#
FilesInput = athenaCommonFlags.BSRDOInput()

doLAr = True
doTile = True

################################################################################
# actual job options
################################################################################

# initial setup
from AthenaCommon.AlgSequence import AlgSequence
from AthenaCommon.AppMgr import ToolSvc,theApp,ServiceMgr
topSequence = AlgSequence()

# setup athenaCommonFlags
from AthenaCommon.AthenaCommonFlags  import athenaCommonFlags
athenaCommonFlags.EvtMax = EvtMax
athenaCommonFlags.SkipEvents = SkipEvents
athenaCommonFlags.FilesInput = FilesInput
del SkipEvents
del EvtMax
del FilesInput

# setup globalflags
from AthenaCommon.GlobalFlags  import globalflags
#globalflags.ConditionsTag.set_Value_and_Lock("COMCOND-BLKPST-005-04")
globalflags.ConditionsTag.set_Value_and_Lock("COMCOND-BLKPA-006-07")

# temporary fix for data12
#from RecExConfig.RecFlags import rec
#rec.projectName.set_Value_and_Lock("data11_calib")

from RecExConfig.AutoConfiguration import ConfigureFromListOfKeys, GetRunNumber
#ConfigureFromListOfKeys(['everything','ConditionsTag=COMCOND-BLKP*-005-08'])
ConfigureFromListOfKeys(['everything'])

# database tag
from IOVDbSvc.CondDB import conddb
conddb.setGlobalTag(globalflags.ConditionsTag())

# setup detflags
import DetDescrCnvSvc.DetStoreConfig
from AthenaCommon.DetFlags import DetFlags
if doLAr: DetFlags.detdescr.LAr_setOn()
if doLAr or doTile: DetFlags.detdescr.Tile_setOn()

# needed ....
from RecExConfig.RecFlags import rec
rec.doLArg.set_Value_and_Lock(doLAr)
rec.doTile.set_Value_and_Lock(doTile)
rec.doCalo.set_Value_and_Lock(doLAr or doTile)
rec.Commissioning.set_Value_and_Lock(True)

# setup geometry
from AtlasGeoModel import SetGeometryVersion
from AtlasGeoModel import GeoModelInit
from AtlasGeoModel import SetupRecoGeometry

# setup bytestream reading
from ByteStreamCnvSvc import ReadByteStream
svcMgr.ByteStreamInputSvc.FullFileName = athenaCommonFlags.FilesInput()
theApp.EvtMax = athenaCommonFlags.EvtMax()
svcMgr.EventSelector.SkipEvents = athenaCommonFlags.SkipEvents()
# Level-1 bs data
include ("TrigT1CaloByteStream/ReadLVL1CaloBS_jobOptions.py")

# detector description
include ("CaloDetMgrDetDescrCnv/CaloDetMgrDetDescrCnv_joboptions.py")
# needed by TrigT1CaloCalibTools/TriggerTowerTools:
include("TileConditions/TileConditions_jobOptions.py")

# setup lar
from LArConditionsCommon.LArCondFlags import larCondFlags
larCondFlags.useShape = True
#larCondFlags.LArCoolChannelSelection="0,1,3:473"

include("LArConditionsCommon/LArConditionsCommon_comm_jobOptions.py")
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

# extra LAr setup
if doLAr:
    include("LArConditionsCommon/LArIdMap_comm_jobOptions.py")
    include("LArIdCnv/LArIdCnv_joboptions.py")
    svcMgr.ByteStreamAddressProviderSvc.TypeNames += ["LArFebHeaderContainer/LArFebHeader"]
    include("LArROD/LArFebErrorSummaryMaker_jobOptions.py")

# cell reconstruction properties
from CaloRec.CaloCellFlags import jobproperties
from TileRecUtils.TileRecFlags import jobproperties
jobproperties.CaloCellFlags.doDeadCellCorr = False
jobproperties.TileRecFlags.readDigits = False
#jobproperties.CaloCellFlags.doLArCreateMissingCells = False
# needed for 17.2.0.2
jobproperties.CaloCellFlags.doPileupOffsetBCIDCorr = False

# reconstruct cells
from CaloRec.CaloCellGetter import CaloCellGetter
CaloCellGetter()
del rec

# setup l1calo database
include('TrigT1CaloCalibConditions/L1CaloCalibConditions_jobOptions.py')
svcMgr.IOVDbSvc.overrideTags +=  ["<prefix>/CALO/Identifier/CaloTTOnOffIdMapAtlas</prefix> <tag>CALOIdentifierCaloTTOnOffIdMapAtlas-0002</tag>"]
svcMgr.IOVDbSvc.overrideTags += ["<prefix>/LAR/Identifier/LArTTCellMapAtlas</prefix> <tag>LARIdentifierLArTTCellMapAtlas-HadFcalFix2</tag>"]

# set up tools
from TrigT1CaloTools.TrigT1CaloToolsConf import LVL1__L1TriggerTowerTool
ToolSvc += LVL1__L1TriggerTowerTool("L1TriggerTowerTool")
from TrigT1CaloCalibTools.TrigT1CaloCalibToolsConf import LVL1__L1CaloLArTowerEnergy
ToolSvc += LVL1__L1CaloLArTowerEnergy("L1CaloLArTowerEnergy")
from TrigT1CaloCalibTools.TrigT1CaloCalibToolsConf import LVL1__L1CaloCells2TriggerTowers
ToolSvc += LVL1__L1CaloCells2TriggerTowers("L1CaloCells2TriggerTowers")
from TrigT1CaloCalibTools.TrigT1CaloCalibToolsConf import LVL1__L1CaloOfflineTriggerTowerTools
ToolSvc += LVL1__L1CaloOfflineTriggerTowerTools("L1CaloOfflineTriggerTowerTools")

# configure actual db maker algorithm
from TrigT1CaloCalibUtils.TrigT1CaloCalibUtilsConf import L1CaloHVCorrectionsForDB
topSequence += L1CaloHVCorrectionsForDB()
from LArRecUtils.LArHVCorrToolDefault import LArHVCorrToolDefault
theLArHVCorrTool = LArHVCorrToolDefault()
ToolSvc += theLArHVCorrTool
topSequence.L1CaloHVCorrectionsForDB.LArHVCorrTool = theLArHVCorrTool

# configure writing of calib database
from RegistrationServices.OutputConditionsAlg import OutputConditionsAlg
HVCorrectionsOutput = OutputConditionsAlg("HVCorrectionsOutput", "dummy.root")
HVCorrectionsOutput.ObjectList = [ "CondAttrListCollection#/TRIGGER/L1Calo/V1/Results/RxLayers",
				   "CondAttrListCollection#/TRIGGER/L1Calo/V1/Results/HVCorrections"]
HVCorrectionsOutput.WriteIOV = True
HVCorrectionsOutput.Run1 = GetRunNumber()
svcMgr.IOVDbSvc.dbConnection="sqlite://;schema=hvcorrections.sqlite;dbname=L1CALO"

print '\n'.join(svcMgr.IOVDbSvc.Folders)
