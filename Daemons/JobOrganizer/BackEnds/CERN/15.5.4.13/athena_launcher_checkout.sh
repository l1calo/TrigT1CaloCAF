export STAGE_SVCCLASS=#INPUT_STAGE_SVC_CLASS#
echo $STAGE_SVCCLASS

export ATLAS_RELEASE=#ATLAS_RELEASE#

source /afs/cern.ch/atlas/software/releases/#ATLAS_RELEASE_NOCACHE#/CMT/v1r20p20090520/mgr/setup.sh

pwd
ls -lrt

export RUNDIR=`pwd`
export CMTDIR=$RUNDIR/cmthome
export TEST_AREA=$RUNDIR/testarea

sed -i "s/#ATLAS_TEST_AREA#/macro ATLAS_TEST_AREA ${PWD//\//\\/}/" requirements

mkdir $TEST_AREA

mkdir $CMTDIR
echo "macro ATLAS_TEST_AREA $TEST_AREA" >> requirements
mv requirements $CMTDIR
cat $CMTDIR/requirements

# somehow things crash if cmt is setup in the same directory athena runs
cd $CMTDIR
cmt config
source setup.sh -tag=#ATLAS_RELEASE#,runtime,oneTest

echo $DATAPATH

echo "TestArea:"
echo $TestArea

mv $RUNDIR/#JOB_OPTIONS_NAME# $TEST_AREA

cd $TestArea
# checkout and comiple packages given as arguments
for package in $*
do
  cmt co $package
  cd $package/cmt
  cmt config
  cmt make
  cd $TestArea
done

echo $PATH

ln -s /afs/cern.ch/atlas/project/tdaq/level1/calo/data/calib/calib.sqlite

# copy input files to local directory
for f in `sed -n '/castor.*data/p' #JOB_OPTIONS_NAME# | sed 's/\s//g' | sed 's/[,"]//g'`
do
    rfcp $f .
done

# change input file names in joboptions file
sed '/castor.*data/s/\"\/.*\//"/g' #JOB_OPTIONS_NAME# > jobo.py

cat jobo.py
ls -lts

athena.py jobo.py | tee #JOB_LOG_NAME#
