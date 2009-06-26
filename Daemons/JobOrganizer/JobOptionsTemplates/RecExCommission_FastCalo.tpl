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

# choose what detector to turn on:
rec.doInDet = False
rec.doLArg = True
rec.doTile = True
rec.doMuon = False
rec.doMuonCombined = False
ATLASCosmicFlags.doLVL1Calo=True
ATLASCosmicFlags.doCTPMon = False
ATLASCosmicFlags.doHLT  = False

athenaCommonFlags.SkipEvents = 0


if 'doAuditors' in dir():
    from RecExConfig.RecFlags  import jobproperties
    jobproperties.Rec.doNameAuditor.set_Value(True)

# input
globalflags.DataSource = 'data'
globalflags.InputFormat = 'bytestream'

#RAW_DATA_SETS#

ATLASCosmicFlags.CosmicSetup = "M8"
# Detector description
globalflags.DetDescrVersion = 'ATLAS-GEO-04-00-00'
jobproperties.BField.solenoidOn=False
jobproperties.BField.barrelToroidOn=True
jobproperties.BField.endcapToroidOn=True
larCondFlags.LArCoolChannelSelection="3:238,306,313,319,325,331,338,344,350,1001:1012,1021,1022"
##        LArCoolChannelSelection="3:238,306,313,319,325,331,338,344,350,1001:1012,1021,1022"
#        ATLASCosmicFlags.doLAr3nsOFCs = True
larCondFlags.OFCShapeFolder='5samples3bins17phases'
ATLASCosmicFlags.doMuonPhysMon = False



ATLASCosmicFlags.NumFile = []

# output
rec.RootNtupleOutput     = "cosmics.ntuple.root"
athenaCommonFlags.PoolESDOutput = "cosmicsESD.pool.root"
ATLASCosmicFlags.FilteredESDOutputFile = "cosmicsESD.filtered.pool.root"
rec.RootHistoOutput  = "monitoring.root"

#Database
ATLASCosmicFlags.IOVDbSvcGlobalTagData = 'COMCOND-ES1C-000-00'

#Steering flags
athenaCommonFlags.EvtMax = 1000000000


rec.doHist=True
ATLASCosmicFlags.doDQMonitoring= False
rec.doWriteESD =False
ATLASCosmicFlags.doFilteredESD=False
rec.doWriteTAG = False

rec.doPerfMon=False
rec.doDetailedPerfMon=False
#more debuginfo
if not RTT:
    rec.doNameAuditor=False
    rec.doDumpProperties=False

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

CBNT_AthenaAware.Members.remove("CBNTAA_CaloCluster/CBNT_EMClusterTopo420Lowcut")
CBNT_AthenaAware.Members.remove("CBNTAA_CaloCell/CBNT_LArCell")
CBNT_AthenaAware.Members.remove("CBNTAA_LArDigits/CBNTAA_LArDigits")
CBNT_AthenaAware.Members.remove("CBNTAA_CaloCluster/CBNT_CaloClusterTopo")
CBNT_AthenaAware.Members.remove("CBNTAA_TileCell/CBNT_DetailedTileCell")
CBNT_AthenaAware.Members.remove("CBNTAA_TileMu/CBNTAA_TileMu")
CBNT_AthenaAware.Members.remove("CBNTAA_TileMuonFitter/CBNTAA_TileMuonFitterHT")
CBNT_AthenaAware.Members.remove("CBNTAA_TileMuROD/CBNTAA_TileMuROD")
CBNT_AthenaAware.Members.remove("CBNTAA_LArMuCandidate/CBNTAA_LArMuCandidate")

#for x in CBNT_AthenaAware.Members:
#        print "toto: " + x
#       if not (x == "CBNTAA_CaloCluster/CBNT_CaloClusterTopo" or x == "CBNTAA_Truth/CBNT_Truth"):
#               CBNT_AthenaAware.Members.remove(x)

for x in topSequence:
        #print "toto: " + x.name()
        if x.name()=="CaloClusterTopoEM420LowcutGetter": x.Enable=False
        if x.name()=="CaloTopoCluster": x.Enable=False
        if x.name()=="CaloCell2TopoClusterMapper": x.Enable=False
        if x.name()=="LArMuIdAlgorithm": x.Enable=False
        if x.name()=="TileLookForMuAlg": x.Enable=False
        if x.name()=="TileMuonFitter": x.Enable=False
        if x.name()=="TileTopoCluster": x.Enable=False
        if x.name()=="TileTowerBuilder": x.Enable=False
        if x.name()=="TileCell2TopoClusterMapper": x.Enable=False
        if x.name()=="LArMonManager": x.Enable=False
        if x.name()=="CaloMonManager": x.Enable=False
        if x.name()=="L1CaloMonManager": x.Enable=False
        if x.name()=="L1MonManager": x.Enable=False
        #if x.name()=="ManagedAthenaMonPilot": x.Enable=False

svcMgr.ByteStreamInputSvc.MaxBadEvents = 100000
