#! usr/bin/env python

"""
    Workflow user submit tasks to manager
    @author: Wei Xu
    @affiliation: CSC @ BNL
    @date created: May 1, 2013
    @data last modified: Jul. 3, 2013

    Useful when as a command line tool
"""

import stomp
import time
import json
import Image
from workflow_listener import Listener

class Workflow_user(Listener):
    def __init__(self, brokers, user, passcode, ssqueues=['/queue/completed'], smqueue='/queue/submitted'):
        """
            initialization
            @param _brokers: broker host and port
            @param _user: listener's username
            @param _passcode: listener's passcode
            @param _connection: current stomp connection
            @param _connected: connection status
            @param _subs_queues: subscribed queues
            @param _subm_queue: submit queue
            @param _listen: listen and wait controller
            """

        self._brokers = brokers
        self._user = user
        self._passcode = passcode
        self._connection = None
        self._connected = False
        self._subs_queues = ssqueues
        self._subm_queue = smqueue
        self._listen = False

    def process(self, filename):
        ###edited by Li
        #_im = Image.open(filename)
        #_im.show()
        return

    def on_message(self, headers, message):
        msg = json.loads(message)
        usr = msg['user']
        filename = msg['output_data_file']
        #print usr, filename
        if usr == self._user:
            print self._user, "got data in", filename
            self.process(filename)
            self._listen = False

    def listen_and_wait(self, waiting_period=1.0):
        if self._connected is False:
            self.connect()
        while(self._connected and self._listen):
            time.sleep(waiting_period)

    def submit(self, message):
        """
            submit mission through message to /queue/submit
        """
        self.connect()
        self.send(self._subm_queue, message)

        self._listen = True
        while(self._listen):
            try:
                self.listen_and_wait()
            except KeyboardInterrupt:
                print "\nStopping"
                self._listen = False
            finally:
                if self._connection is not None and self._connection.is_connected():
                    self._connection.disconnect()
                self._connection = None

