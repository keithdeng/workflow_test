#! usr/bin/ python

"""
    start cluster loop
"""
from workflow.workflow_cluster import Workflow_cluster
from workflow.workflow_setting import brokers

wc = Workflow_cluster(brokers)
wc.start()
