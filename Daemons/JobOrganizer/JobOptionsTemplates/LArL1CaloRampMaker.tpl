################################################################################
# config
################################################################################

ConditionsTag = 'COMCOND-ES1C-003-00'
EvtMax = -1
SkipEvents = 0

from AthenaCommon.AthenaCommonFlags  import athenaCommonFlags
#RAW_DATA_SETS#
FilesInput = athenaCommonFlags.BSRDOInput()

autoConfigPartition = False
doLAr = True
doTile = False

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
#try: # recent switch from RecExCommon to RecExConfig
#    from RecExConfig.AutoConfiguration import ConfigureFieldAndGeo, GetRunNumber
#except:
#    from RecExCommon.AutoConfiguration import ConfigureFieldAndGeo, GetRunNumber
#RunNumber = GetRunNumber()
#ConfigureFieldAndGeo()

import re
RunNumber = int(re.search(r"\.[0-9]{8}\.", FilesInput[0]).group(0)[1:-1])

# configure Field (copy from RecExConfig.AutoConfiguration.GetField()
from AthenaCommon.BFieldFlags import jobproperties
from CoolConvUtilities.MagFieldUtils import getFieldForRun
field = getFieldForRun(RunNumber)
if field.toroidCurrent() > 100:
    jobproperties.BField.barrelToroidOn.set_Value_and_Lock(True)
    jobproperties.BField.endcapToroidOn.set_Value_and_Lock(True)
else:
    jobproperties.BField.barrelToroidOn.set_Value_and_Lock(False)
    jobproperties.BField.endcapToroidOn.set_Value_and_Lock(False)
    
if field.solenoidCurrent() > 100:
    jobproperties.BField.solenoidOn.set_Value_and_Lock(True)
else:
    jobproperties.BField.solenoidOn.set_Value_and_Lock(False)
        
globalflags.DetDescrVersion.set_Value_and_Lock('ATLAS-GEO-08-00-00')
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

svcMgr.PoolSvc.ReadCatalog += [
	"xmlcatalog_file:/afs/cern.ch/atlas/conditions/poolcond/catalogue/fragments/PoolCat_cond09_data.000001.lar.COND_castor.xml",
	"xmlcatalog_file:/afs/cern.ch/atlas/conditions/poolcond/catalogue/fragments/PoolCat_cond09_data.000002.lar.COND_castor.xml"
]

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
topSequence.L1CaloRampMaker.IsGain1 = True
topSequence.L1CaloRampMaker.CheckProvenance = True
# sick tbb board
topSequence.L1CaloRampMaker.SpecialChannelRange = {
	0x1170502 : 100, 0x1170503 : 100, 0x1160402 : 100, 0x1150401 : 100, 0x1160403 : 100, 0x1170403 : 100, 0x1150400 : 100,
	0x1160500 : 100, 0x1160502 : 100, 0x1140503 : 100, 0x1170400 : 100, 0x1140502 : 100, 0x1170401 : 100, 0x1170402 : 100,
	0x1160501 : 100, 0x1140500 : 100, 0x1160503 : 100, 0x1160400 : 100, 0x1160401 : 100, 0x1170500 : 100, 0x1170501 : 100,
	0x1140501 : 100, 0x1150402 : 100, 0x1150403 : 100, 0x1150501 : 100, 0x1150500 : 100, 0x1150502 : 100, 0x1150503 : 100}

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
EnergyScanResultOutput.Run1 = RunNumber
svcMgr.IOVDbSvc.dbConnection="sqlite://;schema=energyscanresults.sqlite;dbname=L1CALO"

# configure writing of additional files for the calibration gui
from TrigT1CaloCalibUtils.L1CaloDumpRampDataAlgorithm import L1CaloDumpRampDataAlgorithm
topSequence += L1CaloDumpRampDataAlgorithm()

print '\n'.join(svcMgr.IOVDbSvc.Folders)
