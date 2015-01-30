"""
Host Finder/Tracker for RPF
"""

from pox.core import core
from pox.host_tracker import host_tracker
from service_thread import ServiceThread
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
import time
import traceback
import logging

log = core.getLogger()

log.setLevel(logging.INFO)

#TODO: To implement
class AttachmentPoints():
    def __init__(self):
        self.hosts = {}     #mac -> dpid

    def _handle_core_ComponentRegistered(self, event):
        if event.name == "host_tracker":
            event.component.addListenerByName("HostEvent", self.__handle_host_tracker_HostEvent)

    def __handle_host_tracker_HostEvent(self, event):
        ip = str(event.entry.ipaddr)
        mac = str(event.entry.macaddr)
        dp_id = dpidToStr(event.entry.dpid)

        print "HOST ATTACHMENTS: ", ip, mac, dp_id

    def update_topology(self):
        pass