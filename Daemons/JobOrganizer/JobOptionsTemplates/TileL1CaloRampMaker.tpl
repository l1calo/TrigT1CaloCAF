################################################################################
# config
################################################################################

ConditionsTag = 'COMCOND-ES1C-003-00'
EvtMax = -1
SkipEvents = 0

from AthenaCommon.AthenaCommonFlags  import athenaCommonFlags
#RAW_DATA_SETS#
FilesInput = athenaCommonFlags.BSRDOInput()

doLAr = False
doTile = True

################################################################################
# actual job options
################################################################################

# initial setup
from AthenaCommon.AlgSequence import AlgSequence
from AthenaCommon.AppMgr import ToolSvc,theApp,ServiceMgr
topSequence = AlgSequence()

# configure database
include('RecJobTransforms/UseOracle.py')

# setup athenaCommonFlags
from AthenaCommon.AthenaCommonFlags  import athenaCommonFlags
athenaCommonFlags.EvtMax = EvtMax
athenaCommonFlags.SkipEvents = SkipEvents
athenaCommonFlags.FilesInput = FilesInput
del SkipEvents
del EvtMax

# setup globalflags
from AthenaCommon.GlobalFlags  import globalflags
globalflags.DetGeo = 'atlas'
globalflags.DataSource = 'data'
globalflags.InputFormat = 'bytestream'
globalflags.ConditionsTag = ConditionsTag if ConditionsTag else 'COMCOND-ES1C-000-00'
del ConditionsTag

# auto config
try: # recent switch from RecExCommon to RecExConfig
    from RecExConfig.AutoConfiguration import ConfigureFieldAndGeo, GetRunNumber, ConfigureConditionsTag
except:
    from RecExCommon.AutoConfiguration import ConfigureFieldAndGeo, GetRunNumber, ConfigureConditionsTag
    
RunNumber = GetRunNumber()
ConfigureFieldAndGeo()

# get run number from input file
#import re
#RunNumber = int(re.search(r"\.[0-9]{8}\.", FilesInput[0]).group(0)[1:-1])
#
## configure Field (copy from RecExConfig.AutoConfiguration.GetField()
#from AthenaCommon.BFieldFlags import jobproperties
#from CoolConvUtilities.MagFieldUtils import getFieldForRun
#field = getFieldForRun(RunNumber)
#if field.toroidCurrent() > 100:
#    jobproperties.BField.barrelToroidOn.set_Value_and_Lock(True)
#    jobproperties.BField.endcapToroidOn.set_Value_and_Lock(True)
#else:	
#    jobproperties.BField.barrelToroidOn.set_Value_and_Lock(False)
#    jobproperties.BField.endcapToroidOn.set_Value_and_Lock(False)
#
#if field.solenoidCurrent() > 100:
#    jobproperties.BField.solenoidOn.set_Value_and_Lock(True)
#else:
#    jobproperties.BField.solenoidOn.set_Value_and_Lock(False)
#
#globalflags.DetDescrVersion.set_Value_and_Lock('ATLAS-GEO-08-00-00')
del FilesInput

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
include("CaloDetMgrDetDescrCnv/CaloDetMgrDetDescrCnv_joboptions.py")
include("LArConditionsCommon/LArConditionsCommon_comm_jobOptions.py")
include("TileIdCnv/TileIdCnv_jobOptions.py")
include("TileConditions/TileConditions_jobOptions.py")
        
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
jobproperties.TileRecFlags.readDigits = True

# reconstruct cells
from CaloRec.CaloCellGetter import CaloCellGetter
CaloCellGetter()
del rec

# setup l1calo database
include('TrigT1CaloCalibConditions/L1CaloCalibConditions_jobOptions.py')
svcMgr.IOVDbSvc.overrideTags +=  ["<prefix>/CALO/Identifier/CaloTTOnOffIdMapAtlas</prefix> <tag>CALOIdentifierCaloTTOnOffIdMapAtlas-0002</tag>"]

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
topSequence.L1CaloRampMaker.IsGain1 = False
# special region 1.3 < |eta| < 1.5, saturation on tile side.
topSequence.L1CaloRampMaker.SpecialChannelRange = { 0x6130f02 : 150, 0x7100003 : 150, 0x7180f03 : 150, 0x7180303 : 150, 0x7100200 : 150,
	0x6130601 : 150, 0x6130302 : 150, 0x61f0303 : 150, 0x71c0e00 : 150, 0x71c0a00 : 150, 0x7180501 : 150, 0x6130003 : 150, 0x7140d01 : 150,
	0x7140600 : 150, 0x7100d00 : 150, 0x6170900 : 150, 0x61b0901 : 150, 0x7180002 : 150, 0x7140c03 : 150, 0x6170901 : 150, 0x6130702 : 150,
	0x7180a00 : 150, 0x61b0403 : 150, 0x6130e00 : 150, 0x7180601 : 150, 0x61f0200 : 150, 0x6130002 : 150, 0x61b0601 : 150, 0x71c0e01 : 150,
	0x7100900 : 150, 0x7100901 : 150, 0x7100501 : 150, 0x6170100 : 150, 0x7140802 : 150, 0x7140003 : 150, 0x7140803 : 150, 0x7180c02 : 150,
	0x7100f02 : 150, 0x61b0b03 : 150, 0x6170302 : 150, 0x6170303 : 150, 0x7180703 : 150, 0x6170b02 : 150, 0x71c0402 : 150, 0x61f0803 : 150,
	0x6170b03 : 150, 0x6130101 : 150, 0x71c0601 : 150, 0x7140702 : 150, 0x61f0500 : 150, 0x71c0403 : 150, 0x71c0501 : 150, 0x7140e00 : 150,
	0x7140703 : 150, 0x7140402 : 150, 0x61f0501 : 150, 0x7140403 : 150, 0x61b0402 : 150, 0x7140e01 : 150, 0x6130703 : 150, 0x7180302 : 150,
	0x61b0a00 : 150, 0x61b0f02 : 150, 0x61b0f03 : 150, 0x7180100 : 150, 0x61b0303 : 150, 0x61f0e01 : 150, 0x71c0b03 : 150, 0x6130d00 : 150,
	0x7180101 : 150, 0x7100c03 : 150, 0x61b0a01 : 150, 0x6170802 : 150, 0x7100d01 : 150, 0x6130500 : 150, 0x7100403 : 150, 0x6130d01 : 150,
	0x7180702 : 150, 0x6170601 : 150, 0x61f0302 : 150, 0x71c0302 : 150, 0x61f0a01 : 150, 0x7180d00 : 150, 0x6130901 : 150, 0x7180d01 : 150,
	0x71c0303 : 150, 0x61f0901 : 150, 0x7140d00 : 150, 0x71c0a01 : 150, 0x7180c03 : 150, 0x6170c03 : 150, 0x6130201 : 150, 0x61b0702 : 150,
	0x71c0b02 : 150, 0x7100b02 : 150, 0x71c0600 : 150, 0x61f0600 : 150, 0x7140901 : 150, 0x61f0f02 : 150, 0x6170702 : 150, 0x6130803 : 150,
	0x6170403 : 150, 0x6170e00 : 150, 0x7180803 : 150, 0x6170703 : 150, 0x71c0c02 : 150, 0x7140f02 : 150, 0x71c0c03 : 150, 0x7100500 : 150,
	0x7140f03 : 150, 0x6130e01 : 150, 0x61b0b02 : 150, 0x6130c02 : 150, 0x6170101 : 150, 0x7100302 : 150, 0x61b0100 : 150, 0x7180003 : 150,
	0x7140501 : 150, 0x7100a00 : 150, 0x6130c03 : 150, 0x71c0900 : 150, 0x7100303 : 150, 0x6170002 : 150, 0x61b0101 : 150, 0x7180802 : 150,
	0x7100b03 : 150, 0x61f0402 : 150, 0x61f0403 : 150, 0x61f0f03 : 150, 0x7180e00 : 150, 0x7100a01 : 150, 0x7100201 : 150, 0x6130402 : 150,
	0x71c0101 : 150, 0x6170d01 : 150, 0x7140c02 : 150, 0x61f0a00 : 150, 0x6130403 : 150, 0x61b0c03 : 150, 0x6170d00 : 150, 0x71c0702 : 150,
	0x6130a01 : 150, 0x71c0d01 : 150, 0x6170c02 : 150, 0x61b0803 : 150, 0x7100600 : 150, 0x6170500 : 150, 0x61f0201 : 150, 0x6130600 : 150,
	0x61b0002 : 150, 0x7180900 : 150, 0x6170501 : 150, 0x7180901 : 150, 0x61b0003 : 150, 0x6130a00 : 150, 0x61f0900 : 150, 0x6170803 : 150,
	0x7140303 : 150, 0x7140100 : 150, 0x71c0200 : 150, 0x7180f02 : 150, 0x7140500 : 150, 0x71c0201 : 150, 0x6170003 : 150, 0x6130200 : 150,
	0x7140601 : 150, 0x6170e01 : 150, 0x61f0b02 : 150, 0x61f0b03 : 150, 0x71c0f02 : 150, 0x61b0e00 : 150, 0x61b0703 : 150, 0x71c0002 : 150,
	0x61b0e01 : 150, 0x7140a01 : 150, 0x6130b02 : 150, 0x71c0802 : 150, 0x7140b02 : 150, 0x71c0803 : 150, 0x7100100 : 150, 0x61f0100 : 150,
	0x61b0900 : 150, 0x7140b03 : 150, 0x71c0003 : 150, 0x6130f03 : 150, 0x7100101 : 150, 0x7140a00 : 150, 0x7140200 : 150, 0x7140201 : 150,
	0x61f0702 : 150, 0x7100802 : 150, 0x61b0d00 : 150, 0x61b0600 : 150, 0x61b0d01 : 150, 0x7180402 : 150, 0x61f0c02 : 150, 0x61f0c03 : 150,
	0x7100703 : 150, 0x61f0002 : 150, 0x6130900 : 150, 0x71c0703 : 150, 0x7180a01 : 150, 0x7180e01 : 150, 0x61f0601 : 150, 0x7140002 : 150,
	0x61f0802 : 150, 0x7100002 : 150, 0x7100c02 : 150, 0x7100f03 : 150, 0x61b0200 : 150, 0x6130100 : 150, 0x6170f02 : 150, 0x6170200 : 150,
	0x61b0201 : 150, 0x6170f03 : 150, 0x6170600 : 150, 0x6130501 : 150, 0x7140900 : 150, 0x61b0501 : 150, 0x71c0901 : 150, 0x7100702 : 150,
	0x61b0500 : 150, 0x7100803 : 150, 0x7180403 : 150, 0x61b0802 : 150, 0x71c0d00 : 150, 0x6130b03 : 150, 0x6130303 : 150, 0x6170201 : 150,
	0x7180600 : 150, 0x61f0003 : 150, 0x7100e01 : 150, 0x7180500 : 150, 0x71c0f03 : 150, 0x6170a00 : 150, 0x61b0c02 : 150, 0x61f0101 : 150,
	0x6170402 : 150, 0x7100402 : 150, 0x6130802 : 150, 0x7100e00 : 150, 0x7140302 : 150, 0x61f0e00 : 150, 0x7180b02 : 150, 0x7180b03 : 150,
	0x71c0500 : 150, 0x7140101 : 150, 0x6170a01 : 150, 0x7180200 : 150, 0x7180201 : 150, 0x61b0302 : 150, 0x61f0703 : 150, 0x71c0100 : 150,
	0x7100601 : 150, 0x61f0d00 : 150, 0x61f0d01 : 150,
	# saturating channels
	0x7120203 : 100, 0x6170c03 : 50, 0x6150b02 : 100, 0x6180d03 : 150}

# configure fitting algorithm
from TrigT1CaloCalibUtils.TrigT1CaloCalibUtilsConf import L1CaloLinearCalibration
topSequence += L1CaloLinearCalibration()

# configure writing of L1CaloRampData.pool.root
from RegistrationServices.OutputConditionsAlg import OutputConditionsAlg
outputConditionsAlg = OutputConditionsAlg("outputConditionsAlg", "L1CaloRampData.pool.root")
outputConditionsAlg.ObjectList = ["L1CaloRampDataContainer"]
outputConditionsAlg.WriteIOV = False

# configure writing of calib database
EnergyScanResultOutput = OutputConditionsAlg("EnergyScanResultOutput", "dummy.root")
EnergyScanResultOutput.ObjectList = ["CondAttrListCollection#/TRIGGER/L1Calo/V1/Results/EnergyScanResults"]
EnergyScanResultOutput.WriteIOV = True
EnergyScanResultOutput.Run1 = RunNumber
svcMgr.IOVDbSvc.dbConnection="sqlite://;schema=energyscanresults.sqlite;dbname=L1CALO"

# configure writing of additional files for the calibration gui
from TrigT1CaloCalibUtils.L1CaloDumpRampDataAlgorithm import L1CaloDumpRampDataAlgorithm
topSequence += L1CaloDumpRampDataAlgorithm()
