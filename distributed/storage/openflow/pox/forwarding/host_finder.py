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
class Hostfinder():
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

    def _update_topology(self):
        log.info("Updating topology")
        """
        topology_map:  {Link(dpid1=5,port1=2, dpid2=3,port2=2): 1422875036.217856, Link(dpid1=5,port1=1, dpid2=2,port2=4): 1422875043.467909, Link(dpid1=3,port1=2, dpid2=5,port2=2): 1422875029.003284, Link(dpid1=4,port1=2, dpid2=3,port2=3): 1422875071.895366, Link(dpid1=4,port1=3, dpid2=5,port2=3): 1422875067.453045, Link(dpid1=6,port1=2, dpid2=4,port2=4): 1422875060.269776, Link(dpid1=2,port1=3, dpid2=6,port2=1): 1422875045.898465, Link(dpid1=5,port1=3, dpid2=4,port2=3): 1422875033.803537, Link(dpid1=6,port1=3, dpid2=5,port2=4): 1422875057.856547, Link(dpid1=6,port1=1, dpid2=2,port2=3): 1422875065.065647, Link(dpid1=2,port1=1, dpid2=3,port2=1): 1422875055.455617, Link(dpid1=5,port1=4, dpid2=6,port2=3): 1422875041.051544, Link(dpid1=3,port1=1, dpid2=2,port2=1): 1422875031.421775, Link(dpid1=2,port1=4, dpid2=5,port2=1): 1422875053.054623, Link(dpid1=4,port1=1, dpid2=2,port2=2): 1422875024.185476, Link(dpid1=3,port1=3, dpid2=4,port2=2): 1422875026.572237, Link(dpid1=2,port1=2, dpid2=4,port2=1): 1422875048.286152, Link(dpid1=4,port1=4, dpid2=6,port2=2): 1422875021.769976}
        topology.keys():  [Link(dpid1=5,port1=2, dpid2=3,port2=2), Link(dpid1=5,port1=1, dpid2=2,port2=4), Link(dpid1=3,port1=2, dpid2=5,port2=2), Link(dpid1=4,port1=2, dpid2=3,port2=3), Link(dpid1=4,port1=3, dpid2=5,port2=3), Link(dpid1=6,port1=2, dpid2=4,port2=4), Link(dpid1=2,port1=3, dpid2=6,port2=1), Link(dpid1=5,port1=3, dpid2=4,port2=3), Link(dpid1=6,port1=3, dpid2=5,port2=4), Link(dpid1=6,port1=1, dpid2=2,port2=3), Link(dpid1=2,port1=1, dpid2=3,port2=1), Link(dpid1=5,port1=4, dpid2=6,port2=3), Link(dpid1=3,port1=1, dpid2=2,port2=1), Link(dpid1=2,port1=4, dpid2=5,port2=1), Link(dpid1=4,port1=1, dpid2=2,port2=2), Link(dpid1=3,port1=3, dpid2=4,port2=2), Link(dpid1=2,port1=2, dpid2=4,port2=1), Link(dpid1=4,port1=4, dpid2=6,port2=2)]
        """

        topology_map = core.openflow_discovery.adjacency #Update the topology calling the param adjacency from Discovery module started in handle()
        self.topology = topology_map.keys() #only the keys have relevant data to this app, the values are the the time since the link was discovered

    def create_syn_request(self, port_num, ip_addr):
        """
        Create an ofp_packet_out to send a syn_request to an endpoint host (client)
        """
        """
        eth = self._create_discovery_packet(dpid, port_num, port_addr, self._ttl)
        po = of.ofp_packet_out(action = of.ofp_action_output(port=port_num))
        po.data = eth.pack()
        return po.pack()
        """
        pass

    def alive(self):
        pass

    def add_host(self):
        pass

    def remove_host(self):
        pass


"""
core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
core.openflow_discovery.addListenerByName("LinkEvent", _handle_LinkEvent)
log.debug("Host_finder component ready")
core.call_when_ready(start_, "openflow_discovery")
"""