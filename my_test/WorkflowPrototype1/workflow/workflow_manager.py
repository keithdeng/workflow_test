#! usr/bin/env python

"""
    Workflow manager dispatching tasks to clusters
    @author: Wei Xu
    @affiliation: CSC @ BNL
    @date created: May 1, 2013
    @data last modified: Jul. 3, 2013
"""

import stomp
import time
import json
import logging
from workflow_listener import Listener
import workflow_setting as wset
from workflow_setting import system_log_file

class Workflow_manager(Listener):
    def __init__(self, brokers, user='admin', passcode='admin', ssqueues=['/queue/submitted', '/queue/cluster-completed'], smqueues=['/queue/completed', '/queue/cluster']):
        """
            initialization
            @param _brokers: broker host and port
            @param _user: listener's username
            @param _passcode: listener's passcode
            @param _connection: current stomp connection
            @param _connected: connection status
            @param _subs_queues: subscribed queues
            @param _subm_queue: submit queue
            """
        
        self._brokers = brokers
        self._user = user
        self._passcode = passcode
        self._connection = None
        self._connected = False
        self._subs_queues = ssqueues
        self._subm_queues = smqueues
    
        logging.basicConfig(filename = system_log_file, format = '%(asctime)s %(message)s', level = logging.INFO)

    def __del__(self):
        self.disconnect()
        logging.info("Manager disconnected.")

    def on_message(self, headers, message):
        _msg = json.loads(message)
        _taskID = _msg['job']
        _userID = _msg['user']
        print self._user, "receives job", _taskID, "from", _userID
        logging.info("received job %s from %s", _taskID, _userID)
        
        destination = headers["destination"]
        if destination == '/queue/submitted':
            if _msg["method"] == "": #empty string means not using user-defined module
                _msg["method"] = wset.module_dict[_taskID]
            _updated_msg = json.dumps(_msg)
            print self._user, "dispatches job to cluster"
            self.send(self._subm_queues[1], _updated_msg) #send to cluster queue
            logging.info("dispatches job to cluster")
        elif destination == '/queue/cluster-completed':
            print self._user, "starts to gather result from cluster"
            self.send(self._subm_queues[0], message) #send to completed queue
            print "-----------------------------------"
            logging.info("starts to gather result from cluster")


    def start(self):
        self.connect()
        _listen = True
        while(_listen):
            try:
                self.listen_and_wait()
            except KeyboardInterrupt:
                print "\nStopping"
                _listen = False
            finally:
                if self._connection is not None and self._connection.is_connected():
                    self._connection.disconnect()
                self._connection = None

        print "Bye bye"

