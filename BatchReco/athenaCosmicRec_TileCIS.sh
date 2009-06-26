#!/usr/local/bin/zsh

#=================================================#
# script for batch reconstruction of cosmic data
#
# damien.prieur@cern.ch
#=================================================#

# the place where you will be launching your jobs
export HOMEDIR=/afs/cern.ch/user/l/l1ccalib
export HOMERECODIR=$HOMEDIR/BatchReco

# where you would like to store the job output files
#export OUTPUTDIR=/castor/cern.ch/user/l/l1ccalib/L1Calo/Commissioning/l1calo

#----------------------------------------------------#

export RUNNUMBER=$1
export TRIGGERTYPE=$2
export JOBPART=$3
export OUTPUTDIR=$4

#if INPUTREC is set, RecExCommon will be taken from user area,
#export INPUTREC=$HOMEDIR/scratch0/L1Calo/Point1Rec/Reconstruction/RecExample/RecExCommission/RecExCommission-00-02-23-53

#if USERAREA is set,  packages checked out and possibly modified
#   by the user will be used directly from batch (without recompilation).
# (They should have
# been compiled against the release being used and should not be
# modified when the job is running)
#export USERAREA=$HOMEDIR/scratch0/L1Calo/Point1Rec


#create clean working directory
if [ -d myjob ] ; then
  echo "##delete already existing myjob directory"
  rm -fR myjob
fi

mkdir myjob
cd myjob

#copy the requirement file from $HOMERECODIR
echo "##copying requirements from $HOMERECODIR"
rfcp $HOMERECODIR/requirements .

echo "##set up cmt"
source /afs/cern.ch/sw/contrib/CMT/v1r20p20070720/mgr/setup.sh
cmt config
which cmt

echo CMTCONFIG=$CMTPATH

# add userarea to CMTPATH
if [ -n "$USERAREA" ] ; then
	source ./setup.sh -tag=14.2.23.2,opt,p1rec,32
  echo "## use user area $USERAREA"
  export CMTPATH=`pwd`:$USERAREA:$CMTPATH
else
  echo "## do not use userarea"
  source ./setup.sh -tag=opt,14.2.23.2,runtime,32
#  export CMTPATH=`pwd`:$CMTPATH
fi
echo "##specified cmt; CMTPATH=$CMTPATH"



if [ -n "$INPUTREC" ]; then
  echo "## Take TestRelease from user area $INPUTREC"
	mkdir run
	cd run

	cp -dp $INPUTREC/cmt/requirements .

	echo "## config"
	cmt config
	echo "##setup.sh"
	source setup.sh
else
	#---------------------------#
	# check out RecExCommission

#	cmt co Reconstruction/RecExample/RecExCommission
#	cd Reconstruction/RecExample/RecExCommission/*/cmt
#	source ./setup.sh
#	gmake
#	cd ../run
#	source ../share/
#	source ../share/RecExCommission_links.sh
#	rm sqlite200
fi


#copy jobOption from $HOMERECODIR
cp $HOMERECODIR/RecExCommission_ATN_TileCIS.py.batch ./RecExCommission_ATN.py


#add file to be processed to the jo
#echo "ATLASCosmicFlags.FullFileName = [\"${INTPUTFILEPATH}\"]" >> RecExCommission_ATN.py

#copy the filelist from $HOMERECODIR to the local folder
#echo "cp $HOMERECODIR/datasetlist_${DATASETNUM}_$JOBPART.py"
cp $HOMERECODIR/datasetlist_${RUNNUMBER}_${TRIGGERTYPE}_${JOBPART}.py ./datasetlist.py

# setup local DB replica
#get_files -jo  RecExCommissionData_links.sh
#cp $HOMERECODIR/RecExCommissionData_links.sh .
source ./RecExCommissionData_links.sh
export STAGE_SVCCLASS=default

# for M6 data on /castor/cern.ch/grid/atlas/DAQ/M6
#export STAGE_SVCCLASS=t0atlas

#run Athena
athena.py RecExCommission_ATN.py | tee log.txt


#----------------------------#
#copy output files to castor

#have to set it back to default to save onto castor
export STAGE_SVCCLASS=default

export OUTPUTPATH=${OUTPUTDIR}/${RUNNUMBER}/${TRIGGERTYPE}

rfdir $OUTPUTPATH
if [ $? -ne 0 ]; then
	echo "=> creating directory"
	rfmkdir -p ${OUTPUTPATH}
	rfmkdir -p ${OUTPUTPATH}/log
fi

rfcp cosmics.ntuple.root ${OUTPUTPATH}/${RUNNUMBER}_${TRIGGERTYPE}_${JOBPART}.cbnt
rfcp log.txt ${OUTPUTPATH}/log/${RUNNUMBER}_${TRIGGERTYPE}_${JOBPART}.log
rfcp RecExCommission_ATN.py ${OUTPUTPATH}/log/${RUNNUMBER}_${TRIGGERTYPE}_${JOBPART}.job


export AFSPATH=${HOMEDIR}/w0/reconstruction/calibration/${RUNNUMBER}/${TRIGGERTYPE}
rfdir $AFSPATH
if [ $? -ne 0 ]; then
	echo "=> creating directory"
	rfmkdir -p ${AFSPATH}
	rfmkdir -p ${AFSPATH}/log
fi

fs setacl ${HOMEDIR}/w0/reconstruction/calibration/${RUNNUMBER} system:anyuser rl
fs setacl ${HOMEDIR}/w0/reconstruction/calibration/${TRIGGERTYPE} system:anyuser rl
fs setacl ${HOMEDIR}/w0/reconstruction/calibration/${TRIGGERTYPE}/log system:anyuser rl

rfcp cosmics.ntuple.root ${AFSPATH}/${RUNNUMBER}_${TRIGGERTYPE}_${JOBPART}.cbnt
rfcp log.txt ${AFSPATH}/log/${RUNNUMBER}_${TRIGGERTYPE}_${JOBPART}.log
rfcp RecExCommission_ATN.py ${AFSPATH}/log/${RUNNUMBER}_${TRIGGERTYPE}_${JOBPART}.job



echo "delete $HOMERECODIR/datasetlist_${RUNNUMBER}_${TRIGGERTYPE}_${JOBPART}.py"
rm $HOMERECODIR/datasetlist_${RUNNUMBER}_${TRIGGERTYPE}_${JOBPART}.py



