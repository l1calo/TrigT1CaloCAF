### To use, please do:
### athena  L1CaloD3PD_RAW_topOptions.py | tee log.raw

l1CaloD3pdOutput="L1CaloD3PD.root"

isCalibrationRun = True

if isCalibrationRun:
   l1CaloD3pdOutput="L1CaloCalibD3PD.root"


### Number of events (-1 = all)
nEvents = -1

### Level of output spewing into the terminal (DEBUG, INFO, WARNING, ERROR, FATAL)
LogLevel = INFO

from RecExConfig.RecFlags  import rec
rec.doTrigger.set_Value_and_Lock(True)
rec.doTile.set_Value_and_Lock(True)
rec.doLArg.set_Value_and_Lock(True)
rec.doInDet.set_Value_and_Lock(False)
rec.doMuon.set_Value_and_Lock(False)

disableRecJobOpts = ('readESD', 'readAOD', 'doTruth', 'doAOD','doAODCaloCells','doAODall','doCBNT',
                    'CBNTAthenaAware','doPerfMon','oldFlagTopSteering','doHist','doDetailedPerfMon',
                    'doWriteAOD','doWriteTAG','doJetMissingETTag','doEgamma',
                    'doMuonCombined','doTau','doMonitoring','doWriteAOD','doWriteESD','doWriteTAG')
for p in disableRecJobOpts:
   getattr(rec, p).set_Value_and_Lock(False)

from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
#RAW_DATA_SETS#
athenaCommonFlags.FilesInput.set_Value_and_Lock(athenaCommonFlags.BSRDOInput())
athenaCommonFlags.EvtMax.set_Value_and_Lock(nEvents)

rec.AutoConfiguration=['everything']

if isCalibrationRun:
   # setup ofc's for LArg
   from LArConditionsCommon.LArCondFlags import larCondFlags
   larCondFlags.useShape = True

   from CaloRec.CaloCellFlags import jobproperties
   from TileRecUtils.TileRecFlags import jobproperties
   jobproperties.CaloCellFlags.doDeadCellCorr = False
   #jobproperties.TileRecFlags.readDigits = False
   jobproperties.CaloCellFlags.doLArCreateMissingCells = False

   # setup trigger
   from TriggerJobOpts.TriggerFlags import TriggerFlags
   TriggerFlags.configurationSourceList.set_Value_and_Lock(['xml'])
   TriggerFlags.doTriggerConfigOnly.set_Value_and_Lock(True)
   TriggerFlags.enableMonitoring.set_Value_and_Lock(False)
   TriggerFlags.dataTakingConditions.set_Value_and_Lock("Lvl1Only")

include ("RecExCommon/RecExCommon_topOptions.py")

svcMgr.IOVDbSvc.overrideTags += ["<prefix>/LAR/Identifier/LArTTCellMapAtlas</prefix> <tag>LARIdentifierLArTTCellMapAtlas-HadFcalFix2</tag>"]
if isCalibrationRun:
   for i in svcMgr.IOVDbSvc.Folders:
      if i.find('PhysWave')> 0: svcMgr.IOVDbSvc.Folders.remove(i)
   conddb.addFolder("LAR_OFL", '/LAR/ElecCalibOfl/OFC/CaliWaveXtalkCorr')
   conddb.addOverride("/LAR/ElecCalibOfl/OFC/CaliWaveXtalkCorr", "LARElecCalibOflOFCCaliWaveXtalkCorr-UPD3-00")

   from glob import glob
   catalog_files = glob("/afs/cern.ch/atlas/conditions/poolcond/catalogue/fragments/PoolCat_cond??_data.??????.lar.COND_castor.xml")
   svcMgr.PoolSvc.ReadCatalog += ["xmlcatalog_file:%s" % i for i in catalog_files]

include("TileRecAlgs/TileCellToTTL1_jobOptions.py")

from L1CaloD3PDMaker.L1CaloD3PD import L1CaloD3PD
alg = L1CaloD3PD(file=l1CaloD3pdOutput,seq=topSequence,level = 2, Database = True, Calibration = isCalibrationRun)

from TrigDecisionTool.TrigDecisionToolConf import Trig__TrigDecisionTool
tdt = Trig__TrigDecisionTool("TrigDecisionTool")
ToolSvc += tdt
tdt.OutputLevel=WARNING
ToolSvc.TrigDecisionTool.Navigation.OutputLevel = WARNING

from TriggerJobOpts.TriggerConfigGetter import TriggerConfigGetter
cfg = TriggerConfigGetter()

topSequence.D3PD.ExistDataHeader = False

if isCalibrationRun:
   # disable reco algorithms for calibration runs
   todis = ('ZdcByteStreamRawData', 'EmTowerBldr', 'LArClusterMaker', 'LAr7_11NocorrClusterMaker', 'LArDigitThinnerFromEMClust', 'CaloTopoCluster', 'CaloCell2TopoCluster', 'CaloClusterTopoEM430Getter', 'EMCell2TopoCluster430', 'TileLookForMuAlg', 'TileMuonFitter', 'ZdcRec')
   for i in todis:
      getattr(topSequence, i).Enable = False
