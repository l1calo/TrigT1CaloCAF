from RecExConfig.RecFlags  import rec
from RecExConfig.RecAlgsFlags import recAlgs
from AthenaCommon.BeamFlags import jobproperties
from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
from AthenaCommon.GlobalFlags import globalflags

rec.AutoConfiguration=["FieldAndGeo"]
jobproperties.Beam.beamType = 'cosmics'
ConditionsTag='COMCOND-ES1C-000-00'

from TriggerJobOpts.TriggerFlags import TriggerFlags as tf
tf.configForStartup.set_Value_and_Lock("HLTonlineNoL1Thr")
tf.configurationSourceList.set_Value_and_Lock(["xml"]) #force xml config

include('RecJobTransforms/UseOracle.py')

rec.readRDO=True
globalflags.InputFormat.set_Value_and_Lock('bytestream')
athenaCommonFlags.BSRDOInput.set_Value_and_Lock(['rfio:/castor/cern.ch/grid/atlas/DAQ/l1calo/00115926/data09_calocomm.00115926.calibration_LarCalibL1Calo.daq.RAW._lb0000._SFI-LVL1-1._0001.data'])
#athenaCommonFlags.BSRDOInput.set_Value_and_Lock(['rfio:/castor/cern.ch/grid/atlas/DAQ/tile/2009/daq/data09_tilecomm.00118508.calibration_tile.daq.RAW._lb0000._TileREB-ROS._0001.data'])

globalflags.ConditionsTag.set_Value_and_Lock(ConditionsTag)
del ConditionsTag

rec.RootNtupleOutput.set_Value_and_Lock("cosmics.ntuple.root")
athenaCommonFlags.PoolESDOutput.set_Value_and_Lock("ESD.pool.root")
rec.RootHistoOutput.set_Value_and_Lock("monitoring.root")

athenaCommonFlags.EvtMax.set_Value_and_Lock(-1)

disableRecJobO = ( 'doTruth', 'doAOD', 'doAODCaloCells', 'doAODall',
                  'CBNTAthenaAware', 'doPerfMon', 'oldFlagTopSteering', 'doHist', 'doDetailedPerfMon',
                  'doWriteAOD', 'doWriteTAG', 'doInDet', 'doMuon', 'doJetMissingETTag', 'doEgamma',
                  'doMuonCombined', 'doTau', 'doMonitoring')
for p in disableRecJobO:
    getattr(rec, p).set_Value_and_Lock(False)
del disableRecJobO

rec.doTile.set_Value_and_Lock(True)
rec.doLArg.set_Value_and_Lock(True)
rec.doCBNT.set_Value_and_Lock(True)

include("RecExCommission/RecExCommissionRepro.py")                

ATLASCosmicFlags.doFilteredESD=False
ATLASCosmicFlags.doCalibFillNt = False
ATLASCosmicFlags.doTrkNtuple = False
ATLASCosmicFlags.doInDetMon = False
ATLASCosmicFlags.doPixelMonitoring = False
ATLASCosmicFlags.doSCTMonitoring = False
ATLASCosmicFlags.doOfflineMonitoring = False
ATLASCosmicFlags.doAlignMonitoring = False
ATLASCosmicFlags.doMuonMon = False
ATLASCosmicFlags.doDQMonitoring = False
ATLASCosmicFlags.doLVL1Calo = True
ATLASCosmicFlags.doCTPMon = False
ATLASCosmicFlags.doHLT = False

from AthenaMonitoring.DQMonFlags import DQMonFlags
DQMonFlags.histogramFile.set_Value_and_Lock( "myMonitoring.root" )

# crashing in 14.5.X VAL 2 3 Feb
include("TrigT1CTMonitoring/CTPFlags.py")
CTPFlags.doCTRDO=False

svcMgr.IOVDbSvc.overrideTags +=  ["<prefix>/CALO/Identifier/CaloTTOnOffIdMapAtlas</prefix> <tag>CALOIdentifierCaloTTOnOffIdMapAtlas-0002</tag>"]

include("RecExCommon/RecExCommon_topOptions.py")

# remove this since no info is stored for this runs in db
svcMgr.IOVDbSvc.Folders.remove("<db>COOLONL_TRIGGER/COMP200</db> /TRIGGER/LVL1/Lvl1ConfigKey <tag>HEAD</tag>")
svcMgr.IOVDbSvc.Folders.remove("<db>COOLONL_TRIGGER/COMP200</db> /TRIGGER/LVL1/Menu <tag>HEAD</tag>")
svcMgr.IOVDbSvc.Folders.remove("<db>COOLONL_TRIGGER/COMP200</db> /TRIGGER/LVL1/Prescales <tag>HEAD</tag>")
svcMgr.IOVDbSvc.FoldersToMetaData.remove("/TRIGGER/LVL1/Lvl1ConfigKey")
svcMgr.IOVDbSvc.FoldersToMetaData.remove("/TRIGGER/LVL1/Menu")
svcMgr.IOVDbSvc.FoldersToMetaData.remove("/TRIGGER/LVL1/Prescales")

# supress error messages
topSequence.TrigBSExtraction.EFResultKey=''
topSequence.TrigBSExtraction.L2ResultKey=''

# disabled not needed algorithms
disabledAlgs = ('CaloTopoCluster', 'CaloCell2TopoCluster', 
                'CaloClusterTopoEM430Getter', 'EMCell2TopoCluster430',
                'TileLookForMuAlg', 'TileMuonFitter', 'RoIBResultToAOD',
                'StreamESD', 'StreamESD_FH')
for x in disabledAlgs:
    getattr(topSequence, x).Enable = False
del disabledAlgs

# disabled CBNT output
disabledCBNTAlgs = ('CBNTAA_CaloCell/CBNT_LArCell',
                    'CBNTAA_LArDigits/CBNTAA_LArDigits',
                    'CBNTAA_TileCell/CBNT_DetailedTileCell',
                    'CBNTAA_CaloCluster/CBNT_CaloClusterTopo',
                    'CBNTAA_CaloCluster/CBNT_EMClusterTopo430',
                    'CBNTAA_TileMu/CBNTAA_TileMu',
                    'CBNTAA_TileMuROD/CBNTAA_TileMuROD',
                    'CBNTAA_TileMuonFitter/CBNTAA_TileMuonFitterHT',
                    'CBNTAA_CaloInfo/CBNT_CaloInfo',
                    'CBNTAA_ReadRoIBResult/CBNT_ReadRoIBResult',
                    'CBNTAA_CaloCluster/CBNT_CaloCluster')
for x in disabledCBNTAlgs:
    topSequence.CBNT_AthenaAware.Members.remove(x)
del disabledCBNTAlgs
