#! usr/bin/ python
"""
    workflow system setting file
    @author: Wei Xu
    @affiliation: CSC @ BNL
    @date created: May 1, 2013
    @data last modified: Jul. 3, 2013
"""

brokers = [('localhost', 61613)]

module_dict = {
    'FBP':'Packages/Tomo/FBP.py',
    'FFT':'Packages/Basic/FFT.py',
    'DPC':'Packages/DPC/DPC.py'
}

data_path = 'Data/'

message_format = {
    "instrument": "HXN",
    "job": "", #FBP, FFT
    "user": "", #user name
    "passcode": "", #user passcode
    "input_data_file": "filename.png", #input filename
    "output_data_file": "ofilename.png", #output filename
    "information": "info msg",
    "method": "", #empty string means use system module instead of self-defined module
    "mode": "local" #processing mode: local vs. cluster
}

system_log_file = 'workflow_manager.log'