#! usr/bin/env python

"""
    Example of a simple non-listening producer
"""
import stomp
import json
import time
import sys
import argparse
from workflow.settings import brokers, icat_user, icat_passcode

class MyListener(object):
    def on_error(self, headers, message):
        print 'User received an error: %s' % message
    
    def on_message(self, headers, message):
        print 'User received a message: %s' % message

def send(destination, message, persistent='true'):
    """
        Send a message to a queue
        @param destination: name of the queue
        @param message: message content
    """
    conn = stomp.Connection(host_and_ports=brokers, 
                    user=icat_user, passcode=icat_passcode, 
                    wait_on_receipt=True)
    conn.start()
    conn.connect()
    conn.send(destination=destination, message=message, persistent=persistent)
    conn.disconnect()

def receive():
    conn = stomp.Connection()
    conn.set_listener('user', MyListener())
    conn.start()
    conn.connect()
    conn.subscribe(destination = '/queue/CATALOG.COMPLETE', ack = 'auto')
    time.sleep(2.0)
    conn.disconnect()
    print 'User exits.'
    
def send_msg(runid=1234, ipts=5678, 
             queue='CATALOG.DATA_READY',
             info=None, error=None,
             data_file='', instrument="HXN"):
    """
        Send simple ActiveMQ message
        @param runid: run number (int)
        @param ipts: IPTS number (int)
        @param queue: ActiveMQ queue to send message to
        @param info: optional information message
        @param error: optional error message
        @param data_file: data file path to be sent in message
        @param instrument: instrument name
    """
    data_dict = {"instrument": instrument,
                 "ipts": "IPTS-%d" % ipts,
                 "run_number": runid,
                 "data_file": data_file}
    
    # Add info/error as needed
    if info is not None:
        data_dict["information"]=info
    if error is not None:
        data_dict["error"]=error

    data = json.dumps(data_dict)
    send(queue, data, persistent='true')
    time.sleep(0.1)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Workflow manager test producer')
    parser.add_argument('-r', metavar='runid', type=int, help='Run number (int)', dest='runid')
    parser.add_argument('-i', metavar='ipts', type=int, help='IPTS number (int)', dest='ipts')
    parser.add_argument('-q', metavar='queue', help='ActiveMQ queue name', dest='queue')
    parser.add_argument('-e', metavar='err', help='Error mesage', dest='err')
    parser.add_argument('-d', metavar='file', help='data file path', dest='file')
    parser.add_argument('-b', metavar='instrument', help='instrument name', dest='instrument')
    namespace = parser.parse_args()
    
    ipts = 5678 if namespace.ipts is None else namespace.ipts
    runid = 1234 if namespace.runid is None else namespace.runid
    queue = 'CATALOG.DATA_READY' if namespace.queue is None else namespace.queue
    file = '' if namespace.file is None else namespace.file
    instrument = 'HXN' if namespace.instrument is None else namespace.instrument
    err = namespace.err
    
    print "Sending %s for IPTS-%g, run %g" % (queue, ipts, runid)
    send_msg(runid, ipts, queue=queue, error=err, data_file=file, instrument=instrument)
    time.sleep(2.0)
    receive()
    

