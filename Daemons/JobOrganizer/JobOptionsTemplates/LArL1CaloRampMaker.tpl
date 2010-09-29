################################################################################
# config
################################################################################

EvtMax = -1
SkipEvents = 0

from AthenaCommon.AthenaCommonFlags  import athenaCommonFlags
#RAW_DATA_SETS#
FilesInput = athenaCommonFlags.BSRDOInput()

doLAr = True
doTile = False

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

from RecExConfig.AutoConfiguration import ConfigureFromListOfKeys, GetRunNumber
ConfigureFromListOfKeys(['everything'])

# database tag
from IOVDbSvc.CondDB import conddb
conddb.setGlobalTag(globalflags.ConditionsTag())

# setup detflags
import DetDescrCnvSvc.DetStoreConfig
from AthenaCommon.DetFlags import DetFlags
if doLAr: DetFlags.detdescr.LAr_setOn()
if doTile: DetFlags.detdescr.Tile_setOn()

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

# setup lar
from LArConditionsCommon.LArCondFlags import larCondFlags
larCondFlags.useShape = True
#larCondFlags.LArCoolChannelSelection="0,1,3:473"

include("LArConditionsCommon/LArConditionsCommon_comm_jobOptions.py")
# use ofc for calib pulses
for i in svcMgr.IOVDbSvc.Folders:
    if i.find('PhysWave')> 0: svcMgr.IOVDbSvc.Folders.remove(i)
conddb.addFolder("LAR_OFL", '/LAR/ElecCalibOfl/OFC/CaliWaveXtalkCorr')
conddb.addOverride("/LAR/ElecCalibOfl/OFC/CaliWaveXtalkCorr", "LARElecCalibOflOFCCaliWaveXtalkCorr-UPD3-00")

from glob import glob
catalog_files = glob("/afs/cern.ch/atlas/conditions/poolcond/catalogue/fragments/PoolCat_cond??_data.??????.lar.COND_castor.xml")

svcMgr.PoolSvc.ReadCatalog += ["xmlcatalog_file:%s" % i for i in catalog_files]

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
jobproperties.CaloCellFlags.doLArCreateMissingCells = False

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
ToolSvc += LVL1__L1TriggerTowerTool()
from TrigT1CaloCalibTools.TrigT1CaloCalibToolsConf import L1CaloLArTowerEnergy
ToolSvc += L1CaloLArTowerEnergy()

# configure actual ramp maker algorithm
import TrigT1CaloCalibUtils
print TrigT1CaloCalibUtils

from TrigT1CaloCalibUtils.TrigT1CaloCalibUtilsConf import L1CaloRampMaker
topSequence += L1CaloRampMaker()
topSequence.L1CaloRampMaker.L1TriggerTowerTool = LVL1__L1TriggerTowerTool()
topSequence.L1CaloRampMaker.DoTile = doTile
topSequence.L1CaloRampMaker.DoLAr = doLAr
topSequence.L1CaloRampMaker.EventsPerEnergyStep = 200
topSequence.L1CaloRampMaker.IsGain1 = True
topSequence.L1CaloRampMaker.CheckProvenance = True

# sick tbb board and saturating LAr
topSequence.L1CaloRampMaker.SpecialChannelRange = {
	0x1170502 : 100, 0x1170503 : 100, 0x1160402 : 100, 0x1150401 : 100, 0x1160403 : 100, 0x1170403 : 100, 0x1150400 : 100,
	0x1160500 : 75, 0x1160502 : 75, 0x1140503 : 100, 0x1170400 : 75, 0x1140502 : 100, 0x1170401 : 100, 0x1170402 : 75,
	0x1160501 : 75, 0x1140500 : 100, 0x1160503 : 75, 0x1160400 : 100, 0x1160401 : 100, 0x1170500 : 100, 0x1170501 : 100,
	0x1140501 : 100, 0x1150402 : 100, 0x1150403 : 100, 0x1150501 : 100, 0x1150500 : 100, 0x1150502 : 100, 0x1150503 : 100,
	0x21d0400 : 150, 0x21d0401 : 150, 0x21d0402 : 150, 
	0x41f0c01 : 70, 0x3130201 : 100, 0x4120603 : 150, 0x4120602 : 150, 0x4130700 : 150, 0x6170503 : 150, 0x41a0800 : 150,
	0x4120d01 : 150, 0x41f0500 : 50, 0x5120602 : 150, 0x51f0801 : 150, 0x5110902 : 50
}

# configure fitting algorithm
from TrigT1CaloCalibUtils.TrigT1CaloCalibUtilsConf import L1CaloLinearCalibration
topSequence += L1CaloLinearCalibration()

# configure writing of L1CaloRampData.pool.root file
from RegistrationServices.OutputConditionsAlg import OutputConditionsAlg
RampDataOutput = OutputConditionsAlg("RampDataOutput", "L1CaloRampData.pool.root")
RampDataOutput.ObjectList = ["L1CaloRampDataContainer"]
RampDataOutput.WriteIOV = False

# configure writing of calib database
EnergyScanResultOutput = OutputConditionsAlg("EnergyScanResultOutput", "dummy.root")
EnergyScanResultOutput.ObjectList = ["CondAttrListCollection#/TRIGGER/L1Calo/V1/Results/EnergyScanResults"]
EnergyScanResultOutput.WriteIOV = True
EnergyScanResultOutput.Run1 = GetRunNumber()
svcMgr.IOVDbSvc.dbConnection="sqlite://;schema=energyscanresults.sqlite;dbname=L1CALO"

# configure writing of additional files for the calibration gui
from TrigT1CaloCalibUtils.L1CaloDumpRampDataAlgorithm import L1CaloDumpRampDataAlgorithm
topSequence += L1CaloDumpRampDataAlgorithm()

print '\n'.join(svcMgr.IOVDbSvc.Folders)
