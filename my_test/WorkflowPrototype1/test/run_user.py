#! usr/bin python

"""
    perform as user
    example for FBP:
    $> python run_user.py xuw FBP "" "output_1.png" 0 180 1
    stands for:        userID job script outputfile related parameters
    example for FFT:
    $> python run_user.py xuw FFT "" "output_fft.png"
    example for DPC:
    $> python run_user.py xuw DPC "" "phi_test.tif"
"""

import time
import stomp
import sys
import json
from workflow.workflow_user import Workflow_user
from workflow.workflow_setting import brokers

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print 'you need to enter at least two arguments! userID and methodID please!'
        exit()

    user = str(sys.argv[1])
    passcode = str(sys.argv[1])
    job = str(sys.argv[2])
    method = ""
    info = ""
    file = "ofilename.png"

    if len(sys.argv) >= 4: #input user defined module file name
        method = str(sys.argv[3])

    if len(sys.argv) == 8: #input also FBP parameters
        file = str(sys.argv[4])
        info = str(sys.argv[5])+' '+str(sys.argv[6])+' '+str(sys.argv[7])
    else:
        file = str(sys.argv[4])
        info = ""

    wu = Workflow_user(brokers, user, passcode)
    message = {"instrument": "HXN",
        "job": job,
        "user": user,
        "passcode": passcode,
        "input_data_file": "filename.png",
        "output_data_file": file,
        "information": info,
        "method": method
    }
    msg = json.dumps(message)
    wu.submit(msg)
