###############################################################################
# config
###############################################################################

EvtMax = -1
SkipEvents = 0

from AthenaCommon.AthenaCommonFlags  import athenaCommonFlags
#RAW_DATA_SETS#
FilesInput = athenaCommonFlags.BSRDOInput()

doLAr = True
doTile = True

# fix vector<vector<int>> problem by instatiating one
v = PyAthena.std.vector(PyAthena.std.vector(int))()

###############################################################################
# actual job options
###############################################################################

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

include("LArConditionsCommon/LArConditionsCommon_comm_jobOptions.py")

# use ofc for calib pulses
#for i in svcMgr.IOVDbSvc.Folders:
#    if i.find('PhysWave')> 0: svcMgr.IOVDbSvc.Folders.remove(i)
#conddb.addFolder("LAR_OFL", '/LAR/ElecCalibOfl/OFC/CaliWaveXtalkCorr')
#conddb.addOverride("/LAR/ElecCalibOfl/OFC/CaliWaveXtalkCorr", "LARElecCalibOflOFCCaliWaveXtalkCorr-UPD3-00")

#from glob import glob
#catalog_files = glob("/afs/cern.ch/atlas/conditions/poolcond/catalogue/fragments/PoolCat_cond??_data.??????.lar.COND_castor.xml")

#svcMgr.PoolSvc.ReadCatalog += ["xmlcatalog_file:%s" % i for i in catalog_files]

include("LArConditionsCommon/LArIdMap_comm_jobOptions.py")
include("LArIdCnv/LArIdCnv_joboptions.py")

# extra LAr setup
if doLAr:
    svcMgr.ByteStreamAddressProviderSvc.TypeNames += ["LArFebHeaderContainer/LArFebHeader"]
    include("LArROD/LArFebErrorSummaryMaker_jobOptions.py")

# extra Tile setup
if doTile:
    include( "TileIdCnv/TileIdCnv_jobOptions.py" )
    include( "TileConditions/TileConditions_jobOptions.py" )
    # fix some strange bug ...
    from TileConditions.TileInfoConfigurator import TileInfoConfigurator
    tileInfoConfigurator = TileInfoConfigurator()
    tileInfoConfigurator.NSamples = 7


from CaloRec.CaloCellFlags import jobproperties
from TileRecUtils.TileRecFlags import jobproperties
jobproperties.CaloCellFlags.doDeadCellCorr = False
#jobproperties.TileRecFlags.readDigits = False
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


include("CBNT_Athena/CBNT_AthenaAware_jobOptions.py")
theApp.HistogramPersistency = "ROOT"
include("CBNT_Athena/CBNT_EventInfo_jobOptions.py")

#doL1CaloCBNT_JEM = False
#doL1CaloCBNT_CPM = False
#doL1CaloCBNT_RODHeader = False
include("TrigT1CaloCalibTools/CBNT_L1Calo_jobOptions.py")
CBNT_AthenaAware.CBNT_L1CaloCPM.L1EmTauTool = ""


from AthenaCommon.AppMgr import ServiceMgr
if not hasattr(ServiceMgr, 'THistSvc'):
    from AthenaCommon import CfgMgr
    ServiceMgr += CfgMgr.THistSvc()
ServiceMgr.THistSvc.Output += ["AANT DATAFILE='%s' OPT='RECREATE'" % 'cosmics.ntuple.root']

from AnalysisTools.AthAnalysisToolsConf import AANTupleStream
theAANTupleStream=AANTupleStream(OutputName='cosmics.ntuple.root')
theAANTupleStream.WriteInputDataHeader = True
theAANTupleStream.ExtraRefNames = []
theAANTupleStream.ExistDataHeader = False
topSequence += theAANTupleStream
