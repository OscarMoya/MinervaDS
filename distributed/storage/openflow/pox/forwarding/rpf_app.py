"""
"""
from pox.core import core
from pox.lib.util import dpidToStr
from service_thread import ServiceThread
from pox.forwarding.rpf import ResilientPathFinder
#from distributed.storage.openflow.pox.forwarding.rpf import ResilientPathFinder
from MinervaDS.distributed.storage.src.config.config import DSConfig
from pox.forwarding.host_finder import Hostfinder
#from distributed.storage.openflow.pox.forwarding.host_finder import Hostfinder

import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

import time
import traceback

import os
import datetime
import numpy
import copy
import logging

log = core.getLogger()

log.setLevel(logging.INFO)

def get_time_now():
    return str(datetime.datetime.now().strftime('%M:%S.%f')[:-3])

class mcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKGREEN = ''
        self.FAIL = ''
        self.ENDC = ''


class ResilientModule(object):

    def __init__(self, ignore=None):
        """
        Initialize

        'proactive' behavior
        'ignore' is an optional list/set of DPIDs to ignore
        """
        log.info(" Initializing Resilient Path Finder")
        core.openflow.addListeners(self)
        self.reactive = False
        self.ignore = set(ignore) if ignore else ()

        self.topology = list()
        self.host_list = list()
        self.priority = 65000 #16777215 # Highest priority

        try:
            self.magic_ip = DSConfig.MAGIC_IP
        except Exception as e:
            log.info(mcolors.FAIL+str(e)+mcolors.ENDC)

        try:
            self.host_finder = Hostfinder()
        except Exception as e:
            log.info(mcolors.FAIL+str(e)+mcolors.ENDC)

        try:
            self.rpf_class = ResilientPathFinder()
        except Exception as e:
            log.info(mcolors.FAIL+str(e)+mcolors.ENDC)

        try:
            core.openflow.addListenerByName("PacketIn", self._handle_PacketIn)
        except Exception as e:
            log.info(mcolors.FAIL+str(e)+mcolors.ENDC)

        """
        try:
            core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
        except Exception as e:
            log.info(e)
        try:
            core.openflow.addListenerByName("LinkEvent", self._handle_LinkEvent)
        except Exception as e:
            log.info(e)
        """

        log.info(mcolors.OKGREEN+" Resilient Path Finder correctly initialized"+mcolors.ENDC)

    def host_search(self, src_ip):
        found = False
        for host in self.host_finder.hosts:
            if host.ip == src_ip:
                found = True
                print "FOUND!"
                return found
            else:
                found = False
                continue
        return found

    def parse_topology(self):
        """
        Process topology list retrieved in get_topology method
        """
        pass

    def get_host_topology(self):
        """
        Call host_finder class to retrieve topology list
        """
        return self.host_finder.hosts

    def get_dpid(self, src_ip):
        dpid = None
        for host in self.host_finder.hosts:
            if host.ip == src_ip:
                print "FOUND!"
                dpid = host.dpid
                return dpid
        return dpid

    def _handle_ConnectionUp(self, event):
        """
        Handle event with Controller Manager
        """
        pass

    def _handle_LinkEvent(self, event):
        """
        TBD???
        """
        pass

    def _handle_PacketIn(self, event, handle_type="PacketIn"):

        log.info("Handling PacketIn")
        eth_headers = event.parse() #Ethernet part of the packet L2
        packet = event.parsed
        log.info("PacketIn Correctly Parsed")

        dpid = event.dpid
        in_port = event.port



        if packet.type == 2054:     #ARP datagram type hex 0806
            print "ARP packet detected!"
            print "packet", packet
            print "header:", eth_headers
            print "header.next:", eth_headers.next

            arp_params = eth_headers.next

            hw_type = arp_params.hwtype     # arp.HW_TYPE_ETHERNET
            proto_type = arp_params.prototype  # arp.PROTO_TYPE_IP
            src_mac = arp_params.hwsrc      # ETHER_ANY
            dst_mac = arp_params.hwdst      # ETHER_ANY
            src_ip = arp_params.protosrc   # IP_ANY
            dst_ip = arp_params.protodst

            print "hw_type", hw_type        # Hardware type, Ethernet = 1
            print "proto_type", proto_type      # Protocol type, IP = 2048
            print "src_mac", src_mac
            print "dst_mac", dst_mac
            print "src_ip", src_ip
            print "dst_ip", dst_ip


            #if dst_ip == self.magic_ip:
            if dst_ip:
                print "HOSTS_LIST", self.host_finder.hosts

                found = self.host_search(src_ip)

                print found
                if not found:
                    log.info(' --> Received packet-in event packet from unknown host')
                    self.host_finder.add_host(src_ip, src_mac, dpid, in_port)
                    #ADD fake dst_ip and dpid to make tests of RFP algorithm
                    "[Host(ip=192.168.1.2, mac=00:00:00:00:00:22, dpid=2, port=5)]"
                    self.host_finder.add_host(dst_ip, src_mac, 6, 2)

                else:
                    print "Host already in list", self.host_finder.hosts



            #else:   # dst_ip != self.magic_ip:
            if dst_ip:
                log.warning(" Couldn't find magic_ip in packet-in event packet")
                self.host_finder.update_topology()
                matrix = self.host_finder.topology_to_matrix()
                #TODO: Trigger RPF for this request
                dpid_src = self.get_dpid(src_ip)
                dpid_dst = self.get_dpid(dst_ip)

                if dpid_src and dpid_dst:
                    #TODO: To implement; Call RPF(topology, src_ip, dst_ip, 3)
                    self.single_rpf(matrix, dpid_src, dpid_dst, 3)
                else:
                    print "dpid_src", dpid_src
                    print "dpid_dst", dpid_dst
                    log.warning(" Couldn't find source or destination DPID")


        elif eth_headers != pkt.ethernet.LLDP_TYPE:     # packet.type != ARP and LLDP
            #self._update_topology()
            vlan_headers = eth_headers.next #VLAN part of the Packet L2
            mpls_headers = vlan_headers.next #MPLS part of the packet L2.5

            """
            vlan_id = vlan_headers.id
            if vlan_id not in [4007,4008,4009]:
                return
            try:
                mpls_label = mpls_headers.label
            except:
                mpls_label = None
            """

            src_mac = packet.src
            dst_mac = packet.dst

            print "pkt type", packet.type

            print "src_mac", src_mac
            print "dst_mac", dst_mac

            print "dpid", dpid
            print "in_port", in_port

            if packet.type == pkt.ethernet.IP_TYPE:

                ipv4_packet = event.parsed.find("ipv4")
                #processing of the IPv4 packet
                src_ip = ipv4_packet.srcip
                dst_ip = ipv4_packet.dstip

                print "src_ip", src_ip
                print "dst_ip", dst_ip

                if dst_ip != self.magic_ip:
                    log.warning("Couldn't find magic_ip in packet-in event packet")
                    #TODO: Trigger RPF for this request
                    #TODO: To implement; Call RPF(topology, src_ip, dst_ip, 3)

                elif dst_ip not in self.host_list:
                    log.info('Received packet-in event packet from unknown host')
                    #TODO: Trigger host_finder, new host connected
                    #self.host_finder.add_host(src_ip, src_mac, dpid, in_port)
                    """
                    mz h1-eth0 -B 192.168.1.3 -t udp "dp=8080, p=A1:00:CC:00:00:AB:CD:EE:EE:DD:DD:00" -v -c 1 -d 1s
                    """

            """
            #self.__route_packet(dpid, in_port, vlan_id, mpls_label, event)
            self.__route_packet(dpid, in_port, event)
            """

    def pos_mapper(self, all_dpids, src, dst):
        pos = 0
        pos_map = dict()

        while all_dpids:
            for dpid in all_dpids:

                print "dpid", dpid

                if dpid == src:
                    print "dpid==src"
                    pos_map = self.dict_mapper(pos, dpid, pos_map)
                    all_dpids.remove(dpid)
                    pos += 1

                elif dpid == dst:
                    print "dpid==dst"
                    continue

                else:
                    print "dpid!=src and dpid!=dst"
                    pos_map = self.dict_mapper(pos, dpid, pos_map)
                    all_dpids.remove(dpid)
                    pos += 1

            if len(all_dpids) == 1:
                print "len(all_dpids)==1"
                print "all_dpids", all_dpids
                if all_dpids.index(dst) == 0:
                    last = all_dpids.pop()
                    pos_map = self.dict_mapper(pos, last, pos_map)
                    print "is all_dpids empty?", all_dpids

            print "pos_map", pos_map

        del all_dpids
        return pos_map


    def dict_mapper(self, position, dpid, mapping):
        try:
            mapping.update({position: dpid})
        except:
            mapping = ({position: dpid})
        return mapping

    def pos_to_dpid(self, paths, mapping):
        ''' Translates the connected DPIDs to its proper DPID number'''

        for path in paths:
            print "path in paths", path
            k = 0
            for index, node in enumerate(path):
                print "index - node", index, node

                if node == 1:
                    dpid = mapping.get(k)
                    print "dpid", dpid
                    path[index] = dpid
                    k += 1
                    print "k", k

                else:
                    k += 1
                    print "k", k
                    continue

            while 0 in path:
                path.remove(0)

        print "paths", paths
        return paths


    #TODO: Given the resilient paths, install proper flowrules per path
    def __flow_pusher(self, src_dpid, dst_dpid, in_port, vlan_id=None, event=None):
        ''' Adds the required rules to the switch flow table'''
        pass

    def single_rpf(self, dpids, src, dst, n_flows):
        """
        Main RPF algorithm process for single location of servers (same dst_dpid); Needed Inputs are:
        - Network topology ()
        - End points (src and dst)
        - Number of resilience flows (current flows=3: A, B, AxB)
        """

        #Network topology should be retrieved from controller and parsed in next format
        """
        dpids = {1: {2: 2, 3: 3, 4: 4, 5: 5},
                2: {1: 1, 3: 3, 4: 4, 5: 5},
                3: {1: 1, 2: 2, 4: 4, 5: 5},
                4: {1: 1, 2: 2, 3: 3, 5: 5},
                5: {1: 1, 2: 2, 3: 3, 4: 4}, }
        """
        arrays = list()

        all_dpids = self.host_finder.get_dpids()
        print "ALL_DPIDS", all_dpids

        num_dpids = len(all_dpids)
        print "num_dpids", num_dpids

        all_dpids_cp = list()
        for dpid in all_dpids:
            all_dpids_cp.append(dpid)

        print "ALL_DPIDS_CP", all_dpids_cp


        pos_dpid_map = self.pos_mapper(all_dpids, src, dst)
        print "pos_dpid_map", pos_dpid_map


        for key in dpids.keys():
            print "KEY: ", key
            print "dpids[key].keys()", dpids[key].keys()

            conn_row = dpids[key].keys()
            print "conn_row", conn_row

            print "all_dpids_cp", all_dpids_cp

            not_conn = list(set(all_dpids_cp)-set(conn_row))

            print "not_connected_set", not_conn

            #conn_row.sort()

            print "conn_row", conn_row  #[2, 4, 5]
            conn_row_len = len(conn_row)
            print "len(conn_row)", conn_row_len

            conn_row_array = numpy.array(conn_row)
            print "conn_row_array", conn_row_array  #[2 4 5]



            conn_row_array = conn_row_array/conn_row_array
            print "conn_row_array/conn_row_array", conn_row_array   #[1 1 1]

            conn_row_list = conn_row_array.tolist()
            print "conn_row_array.tolist", conn_row_list    #[1, 1, 1] -> [1, 1, 1, 0]

            # Check key (dpid)
            # fOR ITEMS in difference: if item != key:
            for item in not_conn:
                print "item, key", item, key
                # get position from pos_dpid_map
                item_pos = pos_dpid_map.values().index(key)
                print "item_pos, item", item_pos, item
                # Add '0' in place of no dpid link
                conn_row_list.insert(item_pos, 0)

            arrays.append(numpy.array(conn_row_list))
            print "arrays.append(numpy.array(conn_row))", arrays

        print "arrays: ", arrays


        #Retrieved topology must be converted into numpy.arrays -> numpy.matrix

        matrix_array = numpy.matrix(arrays)
        print "matrix_array", matrix_array


        a2 = numpy.array([0, 1, 1, 1, 1])
        b2 = numpy.array([1, 0, 1, 1, 1])
        c2 = numpy.array([1, 1, 0, 1, 1])
        d2 = numpy.array([1, 1, 1, 0, 1])
        e2 = numpy.array([1, 1, 1, 1, 0])

        #matrix2 = numpy.matrix([a2,b2,c2,d2,e2,f2,g2])
        matrix2 = numpy.matrix([a2, b2, c2, d2, e2])
        #src_dpid2 = 1
        #dst_dpid2 = 4
        #dst_dpid2 = 7


        print "len(all_dpids_cp)-1", len(all_dpids_cp)-1

        result = self.rpf_class.get_potential_paths(1, len(all_dpids_cp), matrix_array)
        #result = self.rpf_class.get_potential_paths(1, len(all_dpids_cp), matrix2)
        final = list()
        print "result", result

        for r in result:
            if type(r[0]) == list:
                continue
            final.append(r)

        flows = self.rpf_class.flows

        print "final:", final
        len3 = list()
        for i in final:
            if len(i) == 3:
                len3.append(i)
        print len3

        import pprint

        array_list = list()
        for i in final:
            array_list.append(self.rpf_class.generate_adjacency_vector(i, len(all_dpids_cp)))

        print "Array_List: ", array_list
        array_list_2 = list()

        for i in array_list:
            while array_list.count(i) > 1:
                array_list.remove(i)

        for i in array_list:
            array_list_2.append(i[1:len(i)-1])

        pprint.pprint(array_list)
        pprint.pprint(array_list_2)
        mat = numpy.matrix(array_list_2)

        final_result = list()
        orthogonal_vectors = self.rpf_class.get_orthogonal_vectors(mat, 3)
        print "orthogonal_vectors", orthogonal_vectors

        splitter, merger = self.rpf_class.find_places_for_nfs(orthogonal_vectors, 3)

        if splitter and not merger:
            merger = len(all_dpids_cp)
        elif not splitter and not merger:
            merger = len(all_dpids_cp)
            splitter = 1

        for ov in orthogonal_vectors:
            print "OV", ov
            ov.insert(0, 1)     #ov.insert(0, src_dpid2)
            ov.append(1)        #ov.append(dst_dpid2)

        if len(orthogonal_vectors) == flows:
            print "The computated result was that the paths to be taken are: ", orthogonal_vectors  #paths
        else:
            print "Not enough resilient paths calculated, there should be a splitter on node %d and a merger on %d" %(splitter, merger)

        print "ORTHOGONAL_VECTORS: ", orthogonal_vectors

        dpid_paths = self.pos_to_dpid(orthogonal_vectors, pos_dpid_map)

    def multi_rpf(self, dpids, src, dst, n_flows):
        """
        Main RPF algorithm process for multiple location of servers(different dst_dpid); Needed Inputs are:
        - Network topology ()
        - End points (src and (dsts))
        - Number of resilience flows (current flows=3: A, B, AxB)
        """

        #Network topology should be retrieved from controller and parsed in next format
        """
        dpids = {1: {2: 2, 3: 3, 4: 4, 5: 5},
                2: {1: 1, 3: 3, 4: 4, 5: 5},
                3: {1: 1, 2: 2, 4: 4, 5: 5},
                4: {1: 1, 2: 2, 3: 3, 5: 5},
                5: {1: 1, 2: 2, 3: 3, 4: 4}, }
        """
        arrays = list()

        all_dpids = self.host_finder.get_dpids()
        print "ALL_DPIDS", all_dpids

        num_dpids = len(all_dpids)
        print "num_dpids", num_dpids

        all_dpids_cp = list()
        for dpid in all_dpids:
            all_dpids_cp.append(dpid)

        print "ALL_DPIDS_CP", all_dpids_cp


        pos_dpid_map = self.pos_mapper(all_dpids, src, dst)
        print "pos_dpid_map", pos_dpid_map


        for key in dpids.keys():
            print "KEY: ", key
            print "dpids[key].keys()", dpids[key].keys()

            conn_row = dpids[key].keys()
            print "conn_row", conn_row

            print "all_dpids_cp", all_dpids_cp

            not_conn = list(set(all_dpids_cp)-set(conn_row))

            print "not_connected_set", not_conn

            #conn_row.sort()

            print "conn_row", conn_row  #[2, 4, 5]
            conn_row_len = len(conn_row)
            print "len(conn_row)", conn_row_len

            conn_row_array = numpy.array(conn_row)
            print "conn_row_array", conn_row_array  #[2 4 5]



            conn_row_array = conn_row_array/conn_row_array
            print "conn_row_array/conn_row_array", conn_row_array   #[1 1 1]

            conn_row_list = conn_row_array.tolist()
            print "conn_row_array.tolist", conn_row_list    #[1, 1, 1] -> [1, 1, 1, 0]

            # Check key (dpid)
            # fOR ITEMS in difference: if item != key:
            for item in not_conn:
                print "item, key", item, key
                # get position from pos_dpid_map
                item_pos = pos_dpid_map.values().index(key)
                print "item_pos, item", item_pos, item
                # Add '0' in place of no dpid link
                conn_row_list.insert(item_pos, 0)

            arrays.append(numpy.array(conn_row_list))
            print "arrays.append(numpy.array(conn_row))", arrays

        print "arrays: ", arrays


        #Retrieved topology must be converted into numpy.arrays -> numpy.matrix

        matrix_array = numpy.matrix(arrays)
        print "matrix_array", matrix_array


        a2 = numpy.array([0, 1, 1, 1, 1])
        b2 = numpy.array([1, 0, 1, 1, 1])
        c2 = numpy.array([1, 1, 0, 1, 1])
        d2 = numpy.array([1, 1, 1, 0, 1])
        e2 = numpy.array([1, 1, 1, 1, 0])

        #matrix2 = numpy.matrix([a2,b2,c2,d2,e2,f2,g2])
        matrix2 = numpy.matrix([a2, b2, c2, d2, e2])
        #src_dpid2 = 1
        #dst_dpid2 = 4
        #dst_dpid2 = 7


        print "len(all_dpids_cp)-1", len(all_dpids_cp)-1

        result = self.rpf_class.get_potential_paths(1, len(all_dpids_cp), matrix_array)
        #result = self.rpf_class.get_potential_paths(1, len(all_dpids_cp), matrix2)
        final = list()
        print "result", result

        for r in result:
            if type(r[0]) == list:
                continue
            final.append(r)

        flows = self.rpf_class.flows

        print "final:", final
        len3 = list()
        for i in final:
            if len(i) == 3:
                len3.append(i)
        print len3

        import pprint

        array_list = list()
        for i in final:
            array_list.append(self.rpf_class.generate_adjacency_vector(i, len(all_dpids_cp)))

        print "Array_List: ", array_list
        array_list_2 = list()

        for i in array_list:
            while array_list.count(i) > 1:
                array_list.remove(i)

        for i in array_list:
            array_list_2.append(i[1:len(i)-1])

        pprint.pprint(array_list)
        pprint.pprint(array_list_2)
        mat = numpy.matrix(array_list_2)

        final_result = list()
        orthogonal_vectors = self.rpf_class.get_orthogonal_vectors(mat, 3)
        print "orthogonal_vectors", orthogonal_vectors

        splitter, merger = self.rpf_class.find_places_for_nfs(orthogonal_vectors, 3)

        if splitter and not merger:
            merger = len(all_dpids_cp)
        elif not splitter and not merger:
            merger = len(all_dpids_cp)
            splitter = 1

        for ov in orthogonal_vectors:
            print "OV", ov
            ov.insert(0, 1)     #ov.insert(0, src_dpid2)
            ov.append(1)        #ov.append(dst_dpid2)

        if len(orthogonal_vectors) == flows:
            print "The computated result was that the paths to be taken are: ", orthogonal_vectors  #paths
        else:
            print "Not enough resilient paths calculated, there should be a splitter on node %d and a merger on %d" %(splitter, merger)

        print "ORTHOGONAL_VECTORS: ", orthogonal_vectors

        dpid_paths = self.pos_to_dpid(orthogonal_vectors, pos_dpid_map)






################################################
def launch():
    global start_time
    start_time = datetime.datetime.now()
    print "Start Time: ", start_time

    log.info(" Registering Resilient Path Finder")
    core.registerNew(ResilientModule)

    import pox.topology
    #pox.topology.launch()
    import pox.openflow.discovery
    pox.openflow.discovery.launch()
    import pox.openflow.topology
    #pox.openflow.topology.launch()

"""
    import pox.topology
    pox.topology.launch()
    import pox.openflow.discovery
    pox.openflow.discovery.launch()
    import pox.openflow.topology
    pox.openflow.topology.launch()
    log.info("Registering Network Host Tracker")
    pox.host_tracker.launch()
    core.registerNew(attachment)

core.call_when_ready(start_, "openflow_")
"""




