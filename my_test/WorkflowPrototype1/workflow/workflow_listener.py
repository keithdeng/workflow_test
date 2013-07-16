#! usr/bin/env python

"""
    Listener class as base class
    @author: Wei Xu
    @affiliation: CSC @ BNL
    @date created: May 1, 2013
    @data last modified: Jul. 3, 2013
"""

import stomp
import time
import logging
from workflow_setting import system_log_file

#message format
#data_dict = {
    #"instrument": "HXN",
    #"job": "FBP",
    #"user": "user1",
    #"passcode": "passcode",
    #"input_data_file": "filename.png",
    #"output_data_file": "ofilename.png",
    #"information": "info msg"
#}

class Listener(stomp.ConnectionListener):
    def __init__(self, brokers, user, passcode, ssqueues=[], smqueue=''):
        """
            initialization initialize the parameters
            @param _brokers: broker host and port
            @param _user: listener's username
            @param _passcode: listener's passcode
            @param _connection: current stomp connection
            @param _connected: connection status
            @param _subs_queues: subscribed queues
            @param _subm_queue: submit queue
        """
        
        self._brokers = brokers #activemq broker's host and port
        self._user = user #user ID
        self._passcode = passcode #user passcode
        self._connection = None #the connection listened to
        self._connected = False #the connection status
        self._subs_queues = ssqueues #subscribed queues
        self._subm_queue = smqueue #the queue to submit complete msg
    
        logging.basicConfig(filename = system_log_file, format = '%(asctime)s %(message)s', level = logging.INFO)
    
    def __del__(self):
        """
            destructor disconnect the connection
        """
        self.disconnect()
        logging.info("Listener disconnected")
    
    def on_message(self, headers, message):
        print self._user, "receives", message #listener receives msg from queue
        logging.info("Received new message from %s", self._user)
    
    def on_error(self, headers, message):
        print "Hey", self._user, "something is wrong!"
        logging.info("Something is wrong")
      
    def connect(self):
        """
            Connect to a broker
        """
        # Do a clean disconnect first
        self.disconnect()
        # start the connection routine
        conn = stomp.Connection(host_and_ports=self._brokers,
                                user=self._user,
                                passcode=self._passcode,
                                wait_on_receipt=True)
        conn.set_listener('', self)
        conn.start()
        conn.connect()
        for q in self._subs_queues:
            conn.subscribe(destination=q, ack='auto', persistent='true')
            print self._user, "subscribes queue", q
            logging.info("%s subscribes queue %s", self._user, q)
        self._connection = conn
        self._connected = True
        logging.info("Set up connection with broker %s, user %s", self._brokers, self._user)
    
    def disconnect(self):
        """
            Clean disconnect
        """
        if self._connection is not None and self._connection.is_connected():
            self._connection.disconnect()
        self._connection = None
        self._connected = False
        #print self._user, "is disconnected."
        logging.info("Disconnected with broker %s, user %s", self._brokers, self._user)

    def send(self, destination, message, persistent='true'):
        """
            Send a message to a queue
            @param destination: name of the queue
            @param message: message content
        """
        if self._connection is None or self._connected is False:
            conn = stomp.Connection(host_and_ports=self._brokers,
                                    user=self._user, passcode=self._passcode,
                                    wait_on_receipt=True)
            conn.set_listener('', self)
            conn.start()
            conn.connect()
            conn.send(destination=destination, message=message, persistent=persistent)
            conn.disconnect()
        else: #most case
            self._connection.send(destination=destination, message=message, persistent=persistent)
                
        print self._user, "sent a message to", destination
        logging.info("Sent message from %s to %s", self._user, destination)

    def listen_and_wait(self, waiting_period=1.0):
        """
            List for the next message from the brokers
            @param waiting_period: sleep time between connection to a broker
        """
        if self._connected is False:
            self.connect()
        while(self._connected):
            time.sleep(waiting_period)


if __name__ == '__main__':
    print "This is a test."
    conn = Listener([('localhost', 61613)], 'admin', 'admin', ['queue/test'])
    conn.send(destination='queue/test', message='hello test')
    print "done"
