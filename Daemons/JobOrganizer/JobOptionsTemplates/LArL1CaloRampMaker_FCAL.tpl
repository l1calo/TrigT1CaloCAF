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
larCondFlags.useShape = False
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

include("LArConditionsCommon/LArConditionsCommon_comm_jobOptions.py")

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
svcMgr.IOVDbSvc.overrideTags += ["<prefix>/CALO/Identifier/CaloTTOnOffIdMapAtlas</prefix> <tag>CALOIdentifierCaloTTOnOffIdMapAtlas-0002</tag>"]

# get new LAr fcal fix
svcMgr.IOVDbSvc.overrideTags += ["<prefix>/LAR/Identifier/LArTTCellMapAtlas</prefix> <tag>LARIdentifierLArTTCellMapAtlas-HadFcalFix2</tag>"]

# set up tools
from TrigT1CaloTools.TrigT1CaloToolsConf import LVL1__L1TriggerTowerTool
ToolSvc += LVL1__L1TriggerTowerTool()
from TrigT1CaloCalibTools.TrigT1CaloCalibToolsConf import L1CaloLArTowerEnergy
ToolSvc += L1CaloLArTowerEnergy()

# configure actual ramp maker algorithm
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
0x4100001 : 50,
0x4100901 : 50,
0x5100500 : 50,
0x4100101 : 50,
0x5100c00 : 50,
0x4100801 : 50,
0x5100400 : 50,
0x4100f01 : 50,
0x5100b00 : 50,
0x4100701 : 50,
0x5100300 : 50,
0x4100e01 : 50,
0x5100a00 : 50,
0x4100601 : 50,
0x5100200 : 50,
0x4100d01 : 50,
0x5100900 : 50,
0x4100501 : 50,
0x5100100 : 50,
0x4100c01 : 50,
0x5100800 : 50,
0x4100401 : 50,
0x5100f00 : 50,
0x5100000 : 50,
0x4100b01 : 50,
0x5100700 : 50,
0x4100301 : 50,
0x5100e00 : 50,
0x4100a01 : 50,
0x5100600 : 50,
0x4100201 : 50,
0x5100d00 : 50,
0x4100202 : 100,
0x5100603 : 100,
0x4100900 : 100,
0x5100d01 : 100,
0x5180a02 : 100,
0x5180401 : 100,
0x4100203 : 100,
0x4100000 : 100,
0x5100d02 : 100,
0x5180101 : 100,
0x4100002 : 100,
0x5180a03 : 100,
0x4100902 : 100,
0x5100d03 : 100,
0x4180603 : 100,
0x5180201 : 100,
0x4100100 : 100,
0x5100501 : 100,
0x4180601 : 100,
0x4180d02 : 100,
0x5100502 : 100,
0x4180301 : 100,
0x5180203 : 100,
0x4180d03 : 100,
0x5180901 : 100,
0x5100503 : 100,
0x5100303 : 100,
0x4100800 : 100,
0x5100c01 : 100,
0x5180102 : 100,
0x4180501 : 100,
0x5180902 : 100,
0x5100c02 : 100,
0x4180c00 : 100,
0x4100802 : 100,
0x5100c03 : 100,
0x4180503 : 100,
0x4100f00 : 100,
0x4180602 : 100,
0x4180c01 : 100,
0x4100803 : 100,
0x5100401 : 100,
0x4180302 : 100,
0x5180703 : 100,
0x5180500 : 100,
0x4180c02 : 100,
0x5180800 : 100,
0x4180002 : 100,
0x5100402 : 100,
0x5180403 : 100,
0x5180103 : 100,
0x4100f02 : 100,
0x5180200 : 100,
0x4180c03 : 100,
0x4180400 : 100,
0x5180801 : 100,
0x4180f03 : 100,
0x4100f03 : 100,
0x4180d00 : 100,
0x4100700 : 100,
0x5100b01 : 100,
0x4100c02 : 100,
0x4180401 : 100,
0x5180802 : 100,
0x4100003 : 100,
0x5180f00 : 100,
0x5100b02 : 100,
0x4180700 : 100,
0x4180402 : 100,
0x5180803 : 100,
0x4180b00 : 100,
0x5180f01 : 100,
0x4100702 : 100,
0x5100b03 : 100,
0x4180403 : 100,
0x5180001 : 100,
0x4100e00 : 100,
0x4180b01 : 100,
0x5180f02 : 100,
0x4100703 : 100,
0x5100403 : 100,
0x5100301 : 100,
0x4180b02 : 100,
0x5180f03 : 100,
0x5100103 : 100,
0x5100302 : 100,
0x5180003 : 100,
0x4100e02 : 100,
0x4180d01 : 100,
0x4180b03 : 100,
0x5180202 : 100,
0x4180300 : 100,
0x4100a00 : 100,
0x5180701 : 100,
0x4100e03 : 100,
0x4100903 : 100,
0x4100600 : 100,
0x5100a01 : 100,
0x5180702 : 100,
0x4180701 : 100,
0x5180e00 : 100,
0x5100a02 : 100,
0x4180a00 : 100,
0x5180e01 : 100,
0x4180101 : 100,
0x4100602 : 100,
0x5180301 : 100,
0x5100a03 : 100,
0x4180303 : 100,
0x4100d00 : 100,
0x4180a01 : 100,
0x5180e02 : 100,
0x4100603 : 100,
0x5100201 : 100,
0x5180e03 : 100,
0x5180600 : 100,
0x5100202 : 100,
0x4180a02 : 100,
0x4100d02 : 100,
0x4180a03 : 100,
0x4180202 : 100,
0x4180200 : 100,
0x5180601 : 100,
0x5100203 : 100,
0x4180903 : 100,
0x4100d03 : 100,
0x4100500 : 100,
0x5100901 : 100,
0x4180201 : 100,
0x5180602 : 100,
0x4180600 : 100,
0x5180d00 : 100,
0x5100902 : 100,
0x5180300 : 100,
0x5180603 : 100,
0x4180900 : 100,
0x5180000 : 100,
0x5100903 : 100,
0x4100c00 : 100,
0x4180901 : 100,
0x5180d02 : 100,
0x4100503 : 100,
0x5100101 : 100,
0x4180902 : 100,
0x5180d03 : 100,
0x5100102 : 100,
0x4180500 : 100,
0x4180100 : 100,
0x5180501 : 100,
0x4100c03 : 100,
0x4100102 : 100,
0x4100400 : 100,
0x5100801 : 100,
0x5180502 : 100,
0x5180c00 : 100,
0x5100802 : 100,
0x4180102 : 100,
0x5180503 : 100,
0x5180900 : 100,
0x4180800 : 100,
0x5180c01 : 100,
0x4100402 : 100,
0x5100803 : 100,
0x4180103 : 100,
0x4100b00 : 100,
0x5100f01 : 100,
0x4180801 : 100,
0x5180c02 : 100,
0x4100403 : 100,
0x5100001 : 100,
0x5100f02 : 100,
0x4180802 : 100,
0x5180c03 : 100,
0x5180400 : 100,
0x4180f00 : 100,
0x5100002 : 100,
0x4100b02 : 100,
0x5100f03 : 100,
0x4100103 : 100,
0x4180803 : 100,
0x4180000 : 100,
0x4180f01 : 100,
0x5100003 : 100,
0x4100b03 : 100,
0x4100300 : 100,
0x5100701 : 100,
0x5180002 : 100,
0x4180001 : 100,
0x5180402 : 100,
0x4180f02 : 100,
0x5180b00 : 100,
0x5100702 : 100,
0x5180d01 : 100,
0x5180b01 : 100,
0x4100302 : 100,
0x5100703 : 100,
0x5180a00 : 100,
0x4180003 : 100,
0x5100e01 : 100,
0x4180502 : 100,
0x5180b02 : 100,
0x5180903 : 100,
0x5180700 : 100,
0x4100303 : 100,
0x5100e02 : 100,
0x4180702 : 100,
0x5180b03 : 100,
0x4180e00 : 100,
0x5180303 : 100,
0x5180100 : 100,
0x4100a02 : 100,
0x5100e03 : 100,
0x4180703 : 100,
0x4180e01 : 100,
0x4100a03 : 100,
0x4100200 : 100,
0x4180203 : 100,
0x5100601 : 100,
0x5180302 : 100,
0x4180e02 : 100,
0x5100602 : 100,
0x4180e03 : 100,
0x4100502 : 100,
0x5180a01 : 100
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
