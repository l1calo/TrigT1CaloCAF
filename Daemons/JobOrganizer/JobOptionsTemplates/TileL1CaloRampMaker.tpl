################################################################################
# config
################################################################################

ConditionsTag = 'COMCOND-ES1C-000-00'
EvtMax = -1
SkipEvents = 0

from AthenaCommon.AthenaCommonFlags  import athenaCommonFlags
#RAW_DATA_SETS#
FilesInput = athenaCommonFlags.BSRDOInput()

autoConfigPartition = False
doLAr = False
doTile = True

################################################################################
# actual job options
################################################################################

# initial setup
from AthenaCommon.AlgSequence import AlgSequence
from AthenaCommon.AppMgr import ToolSvc,theApp,ServiceMgr
topSequence = AlgSequence()

from AthenaCommon.BeamFlags import jobproperties

# configure database
include('RecJobTransforms/UseOracle.py')

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
globalflags.DetGeo = 'atlas'
globalflags.DataSource = 'data'
globalflags.InputFormat = 'bytestream'
globalflags.ConditionsTag = ConditionsTag if ConditionsTag else 'COMCOND-ES1C-000-00'
del ConditionsTag

# auto config
try: # recent switch from RecExCommon to RecExConfig
    from RecExConfig.AutoConfiguration import ConfigureFieldAndGeo, GetRunNumber
except:
    from RecExCommon.AutoConfiguration import ConfigureFieldAndGeo, GetRunNumber
    
RunNumber = GetRunNumber()
ConfigureFieldAndGeo()

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
rec.doLArg = doLAr
rec.doTile = doTile
rec.doCalo = doLAr or doTile
rec.Commissioning = True

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

# extra Tile setup
if doTile:
    # fix some strange bug ...
    from TileConditions.TileInfoConfigurator import TileInfoConfigurator
    tileInfoConfigurator = TileInfoConfigurator()
    tileInfoConfigurator.NSamples = 7

# reconstruct cells
from CaloRec.CaloCellGetter import CaloCellGetter
CaloCellGetter()
del rec

# setup l1calo database
from IOVDbSvc.CondDB import conddb
L1CaloDbConnection="<dbConnection>sqlite://;schema=calib.sqlite;dbname=L1CALO</dbConnection>"
L1CaloDbTag = "<tag>HEAD</tag>"
L1CaloFolderList = []
L1CaloFolderList += ["/TRIGGER/L1Calo/Configuration/PprChanDefaults"]
L1CaloFolderList += ["/TRIGGER/L1Calo/Calibration/PprChanCalib"]
L1CaloFolderList += ["/TRIGGER/L1Calo/Calibration/PpmDeadChannels"]
for l1calofolder in L1CaloFolderList:
    if not conddb.folderRequested(l1calofolder):
        conddb.addFolder("", L1CaloDbConnection + l1calofolder + L1CaloDbTag)
svcMgr.IOVDbSvc.overrideTags +=  ["<prefix>/CALO/Identifier/CaloTTOnOffIdMapAtlas</prefix> <tag>CALOIdentifierCaloTTOnOffIdMapAtlas-0002</tag>"]

# set up tools
from TrigT1CaloCondSvc.TrigT1CaloCondSvcConf import L1CaloCondSvc
ServiceMgr += L1CaloCondSvc()
from TrigT1CaloTools.TrigT1CaloToolsConf import LVL1__L1TriggerTowerTool
ToolSvc += LVL1__L1TriggerTowerTool()

# configure actual ramp maker algorithm
from TrigT1CaloCalibUtils.TrigT1CaloCalibUtilsConf import L1CaloRampMaker
topSequence += L1CaloRampMaker()
topSequence.L1CaloRampMaker.L1TriggerTowerTool = LVL1__L1TriggerTowerTool()
topSequence.L1CaloRampMaker.DoTile = doTile
topSequence.L1CaloRampMaker.DoLAr = doLAr
topSequence.L1CaloRampMaker.EventsPerEnergyStep = 200

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
EnergyScanResultOutput.ObjectList = ["CondAttrListCollection#/TRIGGER/L1Calo/Results/EnergyScanResults"]
EnergyScanResultOutput.WriteIOV = True
EnergyScanResultOutput.Run1 = RunNumber
svcMgr.IOVDbSvc.dbConnection="sqlite://;schema=energyscanresults.sqlite;dbname=L1CALO"

# configure writing of additional files for the calibration gui
from TrigT1CaloCalibUtils.L1CaloDumpRampDataAlgorithm import L1CaloDumpRampDataAlgorithm
topSequence += L1CaloDumpRampDataAlgorithm()
