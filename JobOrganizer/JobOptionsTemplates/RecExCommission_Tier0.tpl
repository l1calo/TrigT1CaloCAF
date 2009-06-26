if not 'RTT' in dir():
    RTT=False
    if not 'BeamGas' in dir():
        BeamGas = False

if not 'Field' in dir():
    Field=False

if RTT:
    if not 'M4'  in dir():
        M4 = False
    if not 'M6'  in dir():
        M6= False
    if not 'M7'  in dir():
        M7= False
    if not 'M8'  in dir():
        M8= False
    if not 'BeamGas' in dir():
        BeamGas = True


# reduce memory use by not loading all LAr conditions:
from LArConditionsCommon.LArCondFlags import larCondFlags
#larCondFlags.LArCoolChannelSelection="0,3:238"

from AthenaCommon.DetFlags import DetFlags
DetFlags.ID_setOn()

from RecExConfig.RecFlags  import rec
rec.Commissioning=True

# This is an example steering jobOption file for RecExCommission
# More steering flags can be found in RecExCommissionFlags_jobOptions.py

include( "RecExCommission/RecExCommissionCommonFlags_jobOptions.py" )
include( "RecExCommission/RecExCommissionFlags_jobOptions.py" )


if BeamGas:
    jobproperties.Beam.beamType.set_Value_and_Lock("singlebeam")
else:
    jobproperties.Beam.beamType.set_Value_and_Lock("cosmics")


from AthenaCommon.DetFlags import DetFlags
DetFlags.ID_setOn()

# choose what detector to turn on:
ATLASCosmicFlags.doInDet = False
ATLASCosmicFlags.doLAr = False
ATLASCosmicFlags.doTile = False
ATLASCosmicFlags.doMuons = False
ATLASCosmicFlags.doLVL1Calo = True
ATLASCosmicFlags.doCTPMon = True
ATLASCosmicFlags.doHLT  = False


ATLASCosmicFlags.CosmicSetup = "M8"

globalflags.DetDescrVersion = 'ATLAS-GEO-04-00-00'
jobproperties.BField.solenoidOn=False
jobproperties.BField.barrelToroidOn=True
jobproperties.BField.endcapToroidOn=True
larCondFlags.LArCoolChannelSelection="3:238,306,313,319,325,331,338,344,350,1001:1012,1021,1022"
##        LArCoolChannelSelection="3:238,306,313,319,325,331,338,344,350,1001:1012,1021,1022"
#        ATLASCosmicFlags.doLAr3nsOFCs = True
larCondFlags.OFCShapeFolder='5samples3bins17phases'
ATLASCosmicFlags.doMuonPhysMon = False

# for running over data with field on need this to be setto true
if Field:
    globalflags.DetDescrVersion = 'ATLAS-GEO-03-00-00'
    jobproperties.BField.solenoidOn=True
    jobproperties.BField.barrelToroidOn=True
    jobproperties.BField.endcapToroidOn=True



#Database
globalflags.DetDescrVersion = 'ATLAS-CommNF-09-00-00'
#ATLASCosmicFlags.IOVDbSvcGlobalTagData = 'COMCOND-006-01'
#Database
ATLASCosmicFlags.IOVDbSvcGlobalTagData = 'COMCOND-ES1C-000-00'


athenaCommonFlags.EvtMax = 10
athenaCommonFlags.SkipEvents = 0


# input
globalflags.DataSource = 'data'
globalflags.InputFormat = 'bytestream'

athenaCommonFlags.BSRDOInput = [
"/castor/cern.ch/grid/atlas/DAQ/2008/92081/physics_L1Calo/daq.ATLAS.0092081.physics.L1Calo.LB0001.SFO-1._0001.data",
]

ATLASCosmicFlags.NumFile = []

# output
rec.RootNtupleOutput  = "cosmics.ntuple.root"
athenaCommonFlags.PoolESDOutput  = "cosmicsESD.pool.root"
rec.RootHistoOutput  = "monitoring.root"
rec.doHist = False
ATLASCosmicFlags.doDQMonitoring = False
rec.doWriteESD = False
ATLASCosmicFlags.doFilteredESD = False
rec.doWriteTAG = False


ATLASCosmicFlags.doCombinedFit=False
ATLASCosmicFlags.doCaloTrkMuId = False
ATLASCosmicFlags.doDetStatus = False
rec.doPerfMon=False

#Online stuff, all OFF
rec.doJiveXML = False
ATLASCosmicFlags.doOnline = False
ATLASCosmicFlags.OnlineJiveXML = False
ATLASCosmicFlags.AtlantisGeometry = False
ATLASCosmicFlags.CaloDetailedJiveXML = False
ATLASCosmicFlags.doPersint = False


# the main jobOpt
if BeamGas:
    include( "RecExCommission/RecExCommission_SingleBeamtopOptions.py" )
else:
    include( "RecExCommission/RecExCommission_topOptions.py" )



#Over-writes come at the end
MessageSvc = Service("MessageSvc")
MessageSvc.OutputLevel = INFO


# remove stupidly long printout at end of job from THistSvc
Service( "THistSvc" ).OutputLevel = WARNING

#IOVDbSvc.OutputLevel=VERBOSE

# Force usage of the fixed version of the tt on/off id map
svcMgr.IOVDbSvc.overrideTags +=  ["<prefix>/CALO/Identifier/CaloTTOnOffIdMapAtlas</prefix> <tag>CALOIdentifierCaloTTOnOffIdMapAtlas-0002</tag>"]

