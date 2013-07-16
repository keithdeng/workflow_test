#! /bin/bash

##########################################################
## Bash script to run on each core
## 
## @author: Wei Xu
## @affiliation: CSC@BNL
## @date create: Jun. 30, 2013
## @date last modified: Jun. 30, 2013
##########################################################

cd $PBS_O_WORKDIR
PATH=$PBS_O_PATH
#./a.out < mydata.$PBS_VNODENUM

python2.7 single_dpc.py ${PBS_VNODENUM}
