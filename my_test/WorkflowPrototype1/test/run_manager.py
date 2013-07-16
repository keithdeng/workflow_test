#! usr/bin/env python

"""
    start workflow manager loop
"""

from workflow.workflow_manager import Workflow_manager
from workflow.workflow_setting import brokers

wm = Workflow_manager(brokers)
wm.start()
