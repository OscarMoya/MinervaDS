"""
Host Finder/Tracker for RPF
"""
from pox.core import core
from pox.lib.util import dpid_to_str
from collections import namedtuple
import logging

log = core.getLogger()
log.setLevel(logging.INFO)


class Hostfinder():
    def __init__(self):
        self.hosts = list()     #ip -> dpid, port

    def get_dpids(self):
        """
        Return a list with every dpid in topology (keys)
        """
        net_dpids = list()

        for link in self.topology:
            if link.dpid1 not in net_dpids:
                #print "dpid1", link.dpid1
                net_dpids.append(link.dpid1)
            else:
                continue
        #print "net_dpids", net_dpids
        return net_dpids

    def topology_to_matrix(self):

        table = {}

        for link in self.topology:
            #print "link", link
            #print "link.dpid1", link.dpid1
            #print "link.dpid2", link.dpid2
            #print "link.port1", link.port1
            try:
                table[link.dpid1].update({link.dpid2: link.port1})
            except:
                table[link.dpid1] = ({link.dpid2: link.port1})

        #print "TABLE_MATRIX", table
        return table

    def update_topology(self):
        log.info("Updating topology")

        topology_map = core.openflow_discovery.adjacency #Update the topology calling the param adjacency from Discovery module started in handle()
        self.topology = topology_map.keys() #only the keys have relevant data to this app, the values are the the time since the link was discovered

        #Topology result examples:
        """
        topology_map:  {Link(dpid1=5,port1=2, dpid2=3,port2=2): 1422875036.217856, Link(dpid1=5,port1=1, dpid2=2,port2=4): 1422875043.467909, Link(dpid1=3,port1=2, dpid2=5,port2=2): 1422875029.003284, Link(dpid1=4,port1=2, dpid2=3,port2=3): 1422875071.895366, Link(dpid1=4,port1=3, dpid2=5,port2=3): 1422875067.453045, Link(dpid1=6,port1=2, dpid2=4,port2=4): 1422875060.269776, Link(dpid1=2,port1=3, dpid2=6,port2=1): 1422875045.898465, Link(dpid1=5,port1=3, dpid2=4,port2=3): 1422875033.803537, Link(dpid1=6,port1=3, dpid2=5,port2=4): 1422875057.856547, Link(dpid1=6,port1=1, dpid2=2,port2=3): 1422875065.065647, Link(dpid1=2,port1=1, dpid2=3,port2=1): 1422875055.455617, Link(dpid1=5,port1=4, dpid2=6,port2=3): 1422875041.051544, Link(dpid1=3,port1=1, dpid2=2,port2=1): 1422875031.421775, Link(dpid1=2,port1=4, dpid2=5,port2=1): 1422875053.054623, Link(dpid1=4,port1=1, dpid2=2,port2=2): 1422875024.185476, Link(dpid1=3,port1=3, dpid2=4,port2=2): 1422875026.572237, Link(dpid1=2,port1=2, dpid2=4,port2=1): 1422875048.286152, Link(dpid1=4,port1=4, dpid2=6,port2=2): 1422875021.769976}
        topology.keys():  [Link(dpid1=5,port1=2, dpid2=3,port2=2), Link(dpid1=5,port1=1, dpid2=2,port2=4), Link(dpid1=3,port1=2, dpid2=5,port2=2), Link(dpid1=4,port1=2, dpid2=3,port2=3), Link(dpid1=4,port1=3, dpid2=5,port2=3), Link(dpid1=6,port1=2, dpid2=4,port2=4), Link(dpid1=2,port1=3, dpid2=6,port2=1), Link(dpid1=5,port1=3, dpid2=4,port2=3), Link(dpid1=6,port1=3, dpid2=5,port2=4), Link(dpid1=6,port1=1, dpid2=2,port2=3), Link(dpid1=2,port1=1, dpid2=3,port2=1), Link(dpid1=5,port1=4, dpid2=6,port2=3), Link(dpid1=3,port1=1, dpid2=2,port2=1), Link(dpid1=2,port1=4, dpid2=5,port2=1), Link(dpid1=4,port1=1, dpid2=2,port2=2), Link(dpid1=3,port1=3, dpid2=4,port2=2), Link(dpid1=2,port1=2, dpid2=4,port2=1), Link(dpid1=4,port1=4, dpid2=6,port2=2)]
        """

        return


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

    def add_host(self, ip_adr, mac_adr, dpid, port):
        new_host = Host(ip_adr, mac_adr, dpid, port)
        log.info(' Host detected: %s', new_host)
        self.hosts.append(new_host)
        print "new_host: ", new_host
        #print "HOSTS_LIST_UPDATED: ", self.hosts
        #self._update_topology(new_host)
        return

    def remove_host(self, ip_adr):
        for host in self.hosts:
            if host.ip == ip_adr:
                log.info(' Host deleted: %s', host)
                self.hosts.pop(host)
                return


class Link(namedtuple("LinkBase", ("dpid1", "port1", "dpid2", "port2"))):
        @property
        def uni(self):
            """
            Returns a "unidirectional" version of this link
            The unidirectional versions of symmetric keys will be equal
            """
            pairs = list(self.end)
            pairs.sort()
            return Link(pairs[0][0], pairs[0][1], pairs[1][0], pairs[1][1])

        @property
        def end(self):
            return ((self[0], self[1]), (self[2], self[3]))

        def __str__(self):
            return "%s.%s -> %s.%s" % (dpid_to_str(self[0]), self[1],
                                       dpid_to_str(self[2]), self[3])

        def __repr__(self):
            return "Link(dpid1=%s,port1=%s, dpid2=%s,port2=%s)" % (self.dpid1,
            self.port1, self.dpid2, self.port2)

class Host(namedtuple("HostBase", ("ip", "mac", "dpid", "port", "type"))):
        @property
        def end(self):
            return (self[0], self[1], self[2], self[3], self[4])

        def __str__(self):
            return "%s -> %s.%s" % (self[0], dpid_to_str(self[2]), self[3])

        def __repr__(self):
            return "Host(ip=%s, mac=%s, dpid=%s, port=%s, type=%s)" % (self.ip,
            self.mac, self.dpid, self.port, self.type)