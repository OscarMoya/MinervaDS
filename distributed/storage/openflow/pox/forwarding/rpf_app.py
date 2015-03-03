"""
"""

from pox.core import core
from pox.forwarding.rpf import ResilientPathFinder
#from distributed.storage.openflow.pox.forwarding.rpf import ResilientPathFinder
from MinervaDS.distributed.storage.src.config.config import DSConfig
from pox.forwarding.host_finder import Hostfinder
#from distributed.storage.openflow.pox.forwarding.host_finder import Hostfinder
from pox.forwarding.match_manager import Match, MatchManager

import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

import time
import os
import datetime
import numpy
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
        'proactive' behavior
        'ignore' is an optional list/set of DPIDs to ignore
        """
        log.info(" Initializing Resilient Path Finder")
        core.openflow.addListeners(self)
        self.reactive = False
        self.ignore = set(ignore) if ignore else ()

        self.topology = list()
        self.host_list = list()
        self.conn_dpids = dict()
        self.priority = 65000 #16777215 # Highest priority

        self.packet_holder = MatchManager()

        try:
            #self.magic_ip = DSConfig.MAGIC_IP
            self.magic_ip = "192.168.1.254"
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

        try:
            core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
        except Exception as e:
            log.info(e)

        log.info(mcolors.OKGREEN+" Resilient Path Finder correctly initialized"+mcolors.ENDC)

    def host_search(self, src_ip):
        found = False
        for host in self.host_finder.hosts:
            if host.ip == src_ip:
                found = True
                #print "FOUND!"
                return found
            else:
                found = False
                continue
        return found

    def get_host_port(self, ip_address):
        for host in self.host_finder.hosts:
            if host.ip == ip_address:
                return host.dpid, host.port

    def get_host_topology(self):
        """
        Call host_finder class to retrieve topology list
        """
        return self.host_finder.hosts

    def get_dpid(self, src_ip):
        dpid = None
        for host in self.host_finder.hosts:
            if host.ip == src_ip:
                #print "FOUND!"
                dpid = host.dpid
                return dpid
        return dpid

    def compare_dpid(self, dpid_list):
        if len(set(dpid_list)) == 1:
            return True
        else:
            return False

    def _handle_ConnectionUp(self, event):
        """
        Handle event with Controller Manager
        """
        if not event.dpid in self.conn_dpids.keys():
            log.info(" Registering new DPID: %d" % event.dpid)
            self.conn_dpids[event.dpid] = event.connection

    def _handle_PacketIn(self, event, handle_type="PacketIn"):
        log.info("Handling PacketIn")
        eth_headers = event.parse() #Ethernet part of the packet L2
        packet = event.parsed
        #log.info("PacketIn Correctly Parsed")

        dpid = event.dpid
        in_port = event.port

        if packet.type == 2054:     #ARP datagram type hex 0806
            print "ARP packet detected!"
            #print "packet", packet
            #print "header:", eth_headers
            print "header.next:", eth_headers.next

            arp_params = eth_headers.next

            hw_type = arp_params.hwtype     # arp.HW_TYPE_ETHERNET
            proto_type = arp_params.prototype  # arp.PROTO_TYPE_IP
            src_mac = arp_params.hwsrc      # ETHER_ANY
            dst_mac = arp_params.hwdst      # ETHER_ANY
            src_ip = arp_params.protosrc   # IP_ANY
            dst_ip = arp_params.protodst

            """
            print "hw_type", hw_type        # Hardware type, Ethernet = 1
            print "proto_type", proto_type      # Protocol type, IP = 2048
            print "src_mac", src_mac
            print "dst_mac", dst_mac
            print "src_ip", src_ip
            print "dst_ip", dst_ip

            print "dpid", dpid
            print "in_port", in_port
            """

            if dst_ip == self.magic_ip:
                #if dst_ip:
                #print "HOSTS_LIST", self.host_finder.hosts
                found = self.host_search(src_ip)

                #ADD fake dst_ip and dpid to make tests of RFP algorithm
                "[Host(ip=192.168.1.3, mac=00:00:00:00:00:22, dpid=5, port=5)]"
                "[Host(ip=192.168.1.4, mac=00:00:00:00:00:22, dpid=6, port=4)]"
                "[Host(ip=192.168.1.5, mac=00:00:00:00:00:22, dpid=4, port=5)]"

                """
                print mcolors.FAIL+"FAKE_ADDING"+mcolors.ENDC
                if dst_ip == '192.168.1.3':
                    #self.host_finder.add_host(dst_ip, src_mac, 6, 2)
                    self.host_finder.add_host(dst_ip, src_mac, 5, 5)

                if dst_ip == '192.168.1.4':
                    self.host_finder.add_host(dst_ip, src_mac, 6, 4)

                    #self.host_finder.add_host(dst_ip, src_mac, 6, 2)
                if dst_ip == '192.168.1.5':
                    self.host_finder.add_host(dst_ip, src_mac, 4, 5)

                    #self.host_finder.add_host(dst_ip, src_mac, 6, 2)
                """

                if not found:
                    log.info(' --> Received packet-in event packet from unknown host')
                    self.host_finder.add_host(src_ip, src_mac, dpid, in_port)

                else:
                    log.info(' --> Received packet-in event packet from already known host')    #self.host_finder.hosts

            ###########################################################################
            else:   # dst_ip != self.magic_ip:
                #if dst_ip:
                log.warning(" Couldn't find magic_ip in packet-in event packet")

                packet_match = Match()

                packet_match.in_port = in_port
                packet_match.src_mac = src_mac
                packet_match.dst_mac = dst_mac
                packet_match.eth_type = hw_type
                packet_match.vlan_id = None
                packet_match.vlan_priority = None
                packet_match.src_ip = src_ip
                packet_match.dst_ip = dst_ip
                packet_match.ip_tos = None
                packet_match.l3_src_port = None
                packet_match.l3_dst_port = None

                log.warning(" New packet_match")

                self.packet_holder.check_in(packet_match)

                #print "matches", self.packet_holder.matches

                pkt_ready = self.packet_holder.take_off() #list of lists

                self.host_finder.update_topology()
                matrix = self.host_finder.topology_to_matrix()

                #get src and dst dpids, select RPF type
                if pkt_ready:
                    #print "pkt_ready not empty", pkt_ready

                    dsts_ip = list()
                    pkt_root = pkt_ready[0][0].get_root()
                    in_port = pkt_root.get_in_port()
                    src_mac = pkt_root.get_src_mac()
                    eth_type = pkt_root.get_eth_type()
                    vlan_id = pkt_root.get_vlan_id()
                    srcs_ip = pkt_root.get_src_ip()

                    for dsts in pkt_ready:
                        #print "dsts", dsts

                        for match_item in dsts:
                            print mcolors.FAIL+"!!!!!!!!!PACKET_READY!!!!!!!!!!!!"+mcolors.ENDC
                            dsts_ip.append(match_item.get_dst_ip())

                    print "src_ip", srcs_ip
                    print "dst_ip", dsts_ip

                    if type(dsts_ip) is list:

                        dpid_src = self.get_dpid(srcs_ip)
                        print "dpid_src", dpid_src
                        if not dpid_src:
                            log.warning(mcolors.FAIL+" Couldn't find source DPID"+mcolors.ENDC)
                            return

                        dsts_list = list()
                        dsts_dict = dict()
                        for dsts in dsts_ip:
                            dsts_dpid = self.get_dpid(dsts)
                            print "dsts_dpip", dsts_dpid
                            if not dsts_dpid:
                                log.warning(mcolors.FAIL+" Couldn't find destination DPID"+mcolors.ENDC)
                                return
                            else:
                                dsts_list.append(dsts_dpid)
                                dsts_dict[dsts] = dsts_dpid

                        location = self.compare_dpid(dsts_list)

                        #print "IS SINGLE-LOCATION RPF?", location

                        if location:
                            # Call single_RPF(topology, src_ip, dst_ip, 3)
                            result = self.single_rpf(matrix, dpid_src, dsts_list[0], 3)

                            #self.route_flows(result)

                        else:
                            print "dpid_src", dpid_src
                            #print "dpid_dst", dsts_list
                            print "dpid_dst_dict", dsts_dict

                            import threading

                            result_list = list()
                            #print "---------------------TOPO", matrix
                            with threading.Lock():
                                res = self.single_rpf(matrix, dpid_src, dsts_dict[dsts_ip[0]], 3)
                            print "res1", res
                            time.sleep(1)

                            result_list.append(res)
                            #print "---------------------TOPO", matrix
                            with threading.Lock():
                                res = self.single_rpf(matrix, dpid_src, dsts_dict[dsts_ip[1]], 3)
                            print "res2", res
                            time.sleep(1)

                            result_list.append(res)
                            #print "---------------------TOPO", matrix
                            with threading.Lock():
                                res = self.single_rpf(matrix, dpid_src, dsts_dict[dsts_ip[2]], 3)
                            print "res3", res
                            time.sleep(1)

                            result_list.append(res)

                            print "!!!!!!!!!!!!!!!!!!!!!!!!final", result_list
                            print "!!!!!!!!!!!!!!!!!!!!!!!!", dsts_dict

                            print mcolors.FAIL+"!!!!!!!!!MULTI STARTS HERE!!!!!!!!!!!!"+mcolors.ENDC

                            final_result_list = self.multi_rpf(result_list, matrix, dpid_src, None)

                            print "FINAL_RESULT_LIST", final_result_list

                            """
                            for dst_dpid in dsts_list:
                                self.rpf_class = ResilientPathFinder()
                                result = self.single_rpf(matrix, dpid_src, dst_dpid, 3)
                                result_list.append(result)
                            print "result_list", result_list
                            """

                            #final_result_list = [[2, 5], [2, 3, 5, 6], [2, 4]]


                            #self.route_packet(dpid, in_port, vlan_id, mpls_label, event)
                            #self.route_flows(final_result_list, packet_match, srcs_ip, dsts_ip, vlan_id=None, event=None)



            print mcolors.OKGREEN+"----------------------END------------------------"+mcolors.ENDC
            #############################################################################################

        elif eth_headers != pkt.ethernet.LLDP_TYPE:     # packet.type != ARP and LLDP

            #self._update_topology()
            #vlan_headers = eth_headers.next #VLAN part of the Packet L2
            #mpls_headers = vlan_headers.next #MPLS part of the packet L2.5

            """
            vlan_id = vlan_headers.id
            if vlan_id not in [4007,4008,4009]:
                return
            try:
                mpls_label = mpls_headers.label
            except:
                mpls_label = None
            """

            #src_mac = packet.src
            #dst_mac = packet.dst

            """
            print "pkt type", packet.type

            print "src_mac", src_mac
            print "dst_mac", dst_mac

            print "dpid", dpid
            print "in_port", in_port

            log.warning(" Couldn't find source or destination DPID")
            """
            """
            if packet.type == pkt.ethernet.IP_TYPE:

                ipv4_packet = event.parsed.find("ipv4")
                #processing of the IPv4 packet
                src_ip = ipv4_packet.srcip
                dst_ip = ipv4_packet.dstip

                print "src_ip", src_ip
                print "dst_ip", dst_ip

                log.info("Couldn't find magic_ip in packet-in event packet")

                if dst_ip not in self.host_list:
                    log.info('Received packet-in event packet from unknown host')
            """
            """
                    mz h1-eth0 -B 192.168.1.3 -t udp "dp=8080, p=A1:00:CC:00:00:AB:CD:EE:EE:DD:DD:00" -v -c 1 -d 1s
            """
        return

    def pos_mapper(self, all_dpids, src, dst):
        pos = 1
        pos_map = dict()
        pos_rmap = dict()

        print "src: ", src, "dst: ", dst
        #print "pos0==src", src
        pos_map, pos_rmap = self.dict_mapper(1, src, pos_map, pos_rmap)
        all_dpids.remove(src)
        pos += 1

        while all_dpids:
            for dpid in all_dpids:

                #print "dpid", dpid

                if dpid == src:
                    #print "dpid==src", dpid, "==", src
                    continue

                elif dpid == dst:
                    #print "dpid==dst", dpid, "==", dst
                    continue

                else:
                    #print "dpid!=src and dpid!=dst"
                    pos_map, pos_rmap = self.dict_mapper(pos, dpid, pos_map, pos_rmap)
                    all_dpids.remove(dpid)
                    pos += 1

            if len(all_dpids) == 1:
                #print "len(all_dpids)==1"
                #print "all_dpids", all_dpids
                if all_dpids.index(dst) == 0:
                    last = all_dpids.pop()
                    pos_map, pos_rmap = self.dict_mapper(pos, last, pos_map, pos_rmap)
                    #print "is all_dpids empty?", all_dpids

            print "pos_map", pos_map, pos_rmap

        del all_dpids
        return pos_map, pos_rmap

    def dict_mapper(self, position, dpid, mapping=dict(), rmapping=dict()):
        mapping.update({position: dpid})
        rmapping.update({dpid: position})

        return mapping, rmapping

    def pos_to_dpid(self, paths, mapping):
        ''' Translates the connected DPIDs to its proper DPID number'''

        for path in paths:
            #print "path in paths", path
            k = 1
            for index, node in enumerate(path):
                #print "index - node", index, node

                if node == 1:
                    dpid = mapping.get(k)
                    #print "dpid", dpid
                    path[index] = dpid
                    k += 1
                    #print "k", k

                else:
                    k += 1
                    #print "k", k
                    continue

            while 0 in path:
                path.remove(0)

        print "paths", paths
        return paths

    def route_flows(self, paths, matching, src_ip=None, dsts_ip=None, vlan_id=None, event=None):
        ''' Adds the required rules to the switch flow table:
        (final_result_list, packet_match, srcs_ip, dsts_ip)'''
        print mcolors.FAIL+"-------->!!!!!!!!!ROUTE_FLOWS HERE!!!!!!!!!!!!<--------"+mcolors.ENDC

        print "src_ip", src_ip

        src_dpid, src_port = self.get_host_port(src_ip)

        print "src_dpid - src_port", src_dpid, "-", src_port

        links = core.openflow_discovery.adjacency.keys()
        print "links", links

        i = 0
        for path in paths:
            print "path", path
            for dpid in path:
                print "dpid", dpid
                print "dpid_index_in_path", path.index(dpid)

                if path.index(dpid) == 0 and dpid == src_dpid:  #First switch after src
                    print "FIRST"
                    print "i index", i
                    next_dpid = path[path.index(dpid)+1]
                    for link in links:
                        if (link.dpid1 == dpid and link.dpid2 == next_dpid):
                            print "link.dpid1", link.dpid1
                            print "link.dpid2", link.dpid2
                            print "link.port1", link.port1
                            print "link.port2", link.port2
                            print "src_ip", src_ip
                            print "dst_ip", dsts_ip[i]

                            print "self.push_flow(%s, %s, %s, %s, %s, %s, %s)" % (link.dpid1, src_ip, dsts_ip[i], src_port, link.port1, None, None)
                            self.push_flow(link.dpid1, src_ip, dsts_ip[i], src_port, link.port1, None, None)
                            #self.push_flow(dpid_conn, src_dpid, dst_dpid, in_port, out_port, vlan_id, event)

                            break


                elif path.index(dpid) == (len(path)-1):     #last switch before dst
                    print "LAST"
                    print "i index", i
                    for link in links:
                        #print "path[(path.index(dpid))-1]", path[(path.index(dpid))-1]
                        if (link.dpid1 == path[(path.index(dpid))-1] and link.dpid2 == dpid):
                            print "link.dpid1", link.dpid1
                            print "link.dpid2", link.dpid2
                            print "link.port1", link.port1
                            print "link.port2", link.port2
                            print "src_ip", src_ip
                            print "dst_ip", dsts_ip[i]

                            dst_dpid, dst_port = self.get_host_port(dsts_ip[i])
                            print "dst_dpid - dst_port", dst_dpid, "-", dst_port

                            if dst_dpid == link.dpid2:

                                print "self.push_flow(%s, %s, %s, %s, %s, %s, %s)" % (link.dpid2, src_ip, dsts_ip[i], link.port2, dst_port, None, None)
                                self.push_flow(link.dpid2, src_ip, dsts_ip[i], link.port2, dst_port, None, None)
                                #self.push_flow(dpid_conn, src_dpid, dst_dpid, in_port, out_port, vlan_id, event)

                                break

                else:

                    print "MIDDLE"
                    print "i index", i
                    try:
                        next_dpid = path[path.index(dpid)+1]
                        pre_dpid = path[path.index(dpid)-1]
                        for linkx in links:
                            if (linkx.dpid1 == pre_dpid and linkx.dpid2 == dpid):
                                pre_port = linkx.port2
                                print "pre_port = link.port2", pre_port

                                for linky in links:
                                    if (linky.dpid1 == dpid and linky.dpid2 == next_dpid): #or (link.dpid1 == next_dpid and link.dpid2 == dpid):
                                        print "linky.dpid1", linky.dpid1
                                        print "linky.dpid2", linky.dpid2
                                        print "linky.port1", linky.port1
                                        print "linky.port2", linky.port2
                                        print "src_ip", src_ip
                                        print "dst_ip", dsts_ip[i]

                                        print "self.push_flow(%s, %s, %s, %s, %s, %s, %s)" % (linky.dpid1, src_ip, dsts_ip[i], pre_port, linky.port1, None, None)
                                        self.push_flow(linky.dpid1, src_ip, dsts_ip[i], pre_port, linky.port1, None, None)
                                        #self.push_flow(dpid_conn, src_dpid, dst_dpid, in_port, out_port, vlan_id, event)

                                        break
                                break
                    except:

                        break

            i += 1
        return

    def push_flow(self, dpid_conn, src_ip, dst_ip, in_port, out_port, vlan_id=None, event=None):

        # half round trip: TYPE_ETHERNET
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match(in_port=in_port,
                                 dl_type=0x0800,
                                 nw_src=src_ip,
                                 nw_dst=dst_ip)

        # dl_vlan=vlan_id,
        # Use idle and/or hard timeouts to help cleaning the table
        msg.idle_timeout = 200
        msg.hard_timeout = 0  #In order to avoid unnecessary messages between the switches and the controller
        msg.priority = 40
        msg.actions.append(of.ofp_action_output(port=out_port))
        # msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))

        print "DPID_CONN", dpid_conn
        print "CONN_DPIDS", self.conn_dpids
        print "CONN_DPIDS[dpid_conn]", self.conn_dpids[dpid_conn]

        print mcolors.FAIL+"----------->Forward-IP-rule----------->"+mcolors.ENDC
        connection = self.conn_dpids[dpid_conn]
        connection.send(msg)

        # way back trip: TYPE_ETHERNET
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match(in_port=out_port,
                                 dl_type=0x0800,
                                 nw_src=dst_ip,
                                 nw_dst=src_ip)

        # Use idle and/or hard timeouts to help cleaning the table
        msg.idle_timeout = 200
        msg.hard_timeout = 0
        msg.priority = 40
        msg.actions.append(of.ofp_action_output(port=in_port))
        # msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))

        print mcolors.FAIL+"<-----------Reverse-IP-rule<-----------"+mcolors.ENDC
        connection = self.conn_dpids[dpid_conn]
        connection.send(msg)

        # half round trip: TYPE_ARP
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match(in_port=in_port,
                                 dl_type=0x0806,
                                 nw_src=src_ip,
                                 nw_dst=dst_ip)

        # dl_vlan=vlan_id,

        msg.idle_timeout = 200
        msg.hard_timeout = 0
        msg.priority = 40
        msg.actions.append(of.ofp_action_output(port=out_port))

        print mcolors.FAIL+"----------->Forward-ARP-rule----------->"+mcolors.ENDC
        connection = self.conn_dpids[dpid_conn]
        connection.send(msg)

        # way back trip: TYPE_ARP
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match(in_port=out_port,
                                 dl_type=0x0806,
                                 nw_src=dst_ip,
                                 nw_dst=src_ip)

        msg.idle_timeout = 200
        msg.hard_timeout = 0
        msg.priority = 40
        msg.actions.append(of.ofp_action_output(port=in_port))

        print mcolors.FAIL+"<-----------Reverse-ARP-rule<-----------"+mcolors.ENDC
        connection = self.conn_dpids[dpid_conn]
        connection.send(msg)

    def paths_length(self, paths):
        lens_list = list()
        for path_set in paths:
            lens_list.append(len(path_set))

        return lens_list

    def paths_to_arrays(self, paths, dpids):
        #Translate all paths to 0-1 format following a common pattern

        all_dpids = self.host_finder.get_dpids()
        print "dpids.keys", dpids.keys()
        print "dpids_matrix", dpids
        pos = 0

        for path_set in paths:
            arrays = list()

            for path in path_set:
                print "PATH: ", path

                conn_row = path

                print "conn_row", conn_row  #[2, 4, 5]
                print "all_dpids", all_dpids

                not_conn = list(set(all_dpids)-set(conn_row))

                print "not_connected_set", not_conn

                conn_row_array = numpy.array(conn_row)
                #print "conn_row_array", conn_row_array  #[2 4 5]

                conn_row_array = conn_row_array/conn_row_array
                #print "conn_row_array/conn_row_array", conn_row_array   #[1 1 1]

                conn_row_list = conn_row_array.tolist()
                #print "conn_row_array.tolist", conn_row_list    #[1, 1, 1] -> [1, 1, 1, 0]

                # ITEMS in difference:
                for item in not_conn:
                    print "item, key", item, path
                    # get position from pos_dpid_map
                    #item_pos = pos_dpid_map.values().index(item)
                    item_pos = dpids.keys().index(item)
                    print "item, item_position", item, item_pos
                    # Add '0' in place of no dpid link
                    conn_row_list.insert(item_pos, 0)
                    print "current_conn_row_list", conn_row_list

                #print "conn_row_list", conn_row_list
                arrays.append(numpy.array(conn_row_list))
                #print "arrays.append(numpy.array(conn_row))", arrays
            pos += 1
            print "POSITION", pos

            if pos == 1:
                A_arrays = arrays
            elif pos == 2:
                B_arrays = arrays
            elif pos == 3:
                C_arrays = arrays

        return A_arrays, B_arrays, C_arrays

    def matrixer(self, arrays, index):
        matrix_array = numpy.matrix(arrays)
        print "matrix_array", matrix_array

        path_row_list = list()
        for a in arrays:
            row = a.tolist()
            path_row_list.append(row)

        print "result -> PATH_ROW_LIST", path_row_list

        final = list()

        for r in path_row_list:
            if type(r[0]) == list:
                continue
            final.append(r)
            print "for_final", final

        flows = self.rpf_class.flows

        #print "final:", final
        len3 = list()
        for i in final:
            if len(i) == 3:
                len3.append(i)
                print "len3", len3
        import pprint

        array_list = list()
        print "--------------------------------------->>>final", final

        #Delete all srcs for each mat row
        import pprint

        """
        array_list = list()
        for i in final:
            array_list.append(self.rpf_class.generate_adjacency_vector(i, len(all_dpids)))   #number of dpids
        """
        #Delete only the src column and delete possible repeated vectors:
        #print "array_list", array_list
        array_list_2 = list()

        """
        for i in array_list:
            while array_list.count(i) > 1:
                array_list.remove(i)
        """

        for i in final:
            nw_list = list()
            pos = 0
            for j in i:
                if pos != index:
                    nw_list.append(j)
                    pos += 1
                else:
                    pos += 1

            #array_list_2.append(i[1:len(i)])
            array_list_2.append(nw_list)

        #pprint.pprint(array_list)
        pprint.pprint(array_list_2)

        #And then, the magic of multi RPF starts below!
        ##
        # creating matrix

        mat = numpy.matrix(array_list_2)
        return mat

    def single_rpf(self,  dpids, src, dst, n_flows=None):
        """
        Main RPF algorithm process for single location of servers (same dst_dpid); Needed Inputs are:
        - Network topology ()
        - End points (src and dst)
        - Number of resilience flows (current flows=3: A, B, AxB)
        """

        #Network topology should be retrieved from controller and parsed in next format
        arrays = list()

        all_dpids = self.host_finder.get_dpids()
        #print "ALL_DPIDS", all_dpids

        pos_dpid_map, dpid_pos_map = self.pos_mapper(all_dpids, src, dst)
        print "pos_dpid_map", pos_dpid_map
        print "dpid_pos_map", dpid_pos_map

        print "dpids_matrix", dpids

        #Network topology should be retrieved from controller and parsed in next format
        """
        dpids = {1: {2: 2, 3: 3, 4: 4, 5: 5},
                2: {1: 1, 3: 3, 4: 4, 5: 5},
                3: {1: 1, 2: 2, 4: 4, 5: 5},
                4: {1: 1, 2: 2, 3: 3, 5: 5},
                5: {1: 1, 2: 2, 3: 3, 4: 4},}
        """

        #all_dpids_cp = self.host_finder.get_dpids()
        all_dpids_cp = pos_dpid_map.keys()
        print "ALL_DPIDS_CP", all_dpids_cp
        num_dpids = len(all_dpids_cp)
        #print "num_dpids", num_dpids

        dpid_keys = pos_dpid_map.values()
        #dpid_keys.sort()
        print "dpid_keys", dpid_keys

        for key in dpid_keys:
            print "KEY: ", key
            print "dpids[key].keys()", dpids[key].keys()

            conn_row = dpids[key].keys()

            print "conn_row", conn_row

            for item in conn_row:
                print "item", item
                replace = dpid_pos_map.get(item)
                print "replace", replace
                oldindex = conn_row.index(item)
                print "oldindex", oldindex
                conn_row.insert(oldindex, replace)
                print "working_conn_row", conn_row
                conn_row.pop(conn_row.index(item))

            print "------->ALTERED_conn_row", conn_row

            #print "all_dpids_cp", all_dpids_cp

            not_conn = list(set(all_dpids_cp)-set(conn_row))

            #print "not_connected_set", not_conn

            #conn_row.sort()

            #print "conn_row", conn_row  #[2, 4, 5]
            conn_row_len = len(conn_row)
            #print "len(conn_row)", conn_row_len

            conn_row_array = numpy.array(conn_row)
            #print "conn_row_array", conn_row_array  #[2 4 5]

            conn_row_array = conn_row_array/conn_row_array
            #print "conn_row_array/conn_row_array", conn_row_array   #[1 1 1]

            conn_row_list = conn_row_array.tolist()
            #print "conn_row_array.tolist", conn_row_list    #[1, 1, 1] -> [1, 1, 1, 0]

            # Check key (dpid)
            # fOR ITEMS in difference: if item != key:
            for item in not_conn:
                print "item, key", item, key
                # get position from pos_dpid_map
                #item_pos = pos_dpid_map.values().index(item)
                item_pos = item - 1
                print "item, item_position", item, item_pos
                # Add '0' in place of no dpid link
                conn_row_list.insert(item_pos, 0)
                print "current_conn_row_list", conn_row_list

            #print "conn_row_list", conn_row_list
            arrays.append(numpy.array(conn_row_list))
            #print "arrays.append(numpy.array(conn_row))", arrays

        print "arrays: ", arrays


        #Retrieved topology must be converted into numpy.arrays -> numpy.matrix

        matrix_array = numpy.matrix(arrays)
        print "pos_dpid_map", pos_dpid_map
        print "matrix_array", matrix_array

        result = self.rpf_class.get_potential_paths(1, len(all_dpids_cp), matrix_array)
        #result = self.rpf_class.get_potential_paths(1, len(all_dpids_cp), matrix_array, list(), list())
        #print "RESULT", result
        #result = self.rpf_class.get_potential_paths(1, len(all_dpids_cp), matrix2)
        final = list()
        #print "result", result

        for r in result:
            if type(r[0]) == list:
                continue
            final.append(r)

        flows = self.rpf_class.flows

        #print "final:", final
        len3 = list()
        for i in final:
            if len(i) == 3:
                len3.append(i)

        import pprint

        array_list = list()
        print "--------------------------------------->>>final", final
        for i in final:
            array_list.append(self.rpf_class.generate_adjacency_vector(i, len(all_dpids_cp)))

        #print "Array_List: ", array_list
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
        pos_dpid_map = {}
        print "dpid_paths", dpid_paths

        return dpid_paths

    def multi_rpf(self, paths, dpids, src, dst):
        """
        Second RPF algorithm process for multiple location of servers(different dst_dpid); Needed Inputs are:
        - Resilient paths
        - Network topology ()
        - End points (src and (dsts))
        """
        print "ALL_DPIDS", dpids.keys()

        print "dpids_matrix", dpids
        print "dpid SOURCE", src

        print "src-INDEX", dpids.keys().index(src)
        src_index = dpids.keys().index(src)

        A_array, B_array, C_array = self.paths_to_arrays(paths, dpids)

        print "ARRAY A", A_array
        print "ARRAY B", B_array
        print "ARRAY C", C_array

        lengths = self.paths_length(paths)
        print "LENGTHS", lengths

        #Create matrixes

        A_matrix = self.matrixer(A_array, src_index)
        B_matrix = self.matrixer(B_array, src_index)
        C_matrix = self.matrixer(C_array, src_index)

        print "MATRIX A", A_matrix
        print "MATRIX B", B_matrix
        print "MATRIX C", C_matrix

        print "BuC Array", B_array+C_array
        print "AuC Array", A_array+C_array

        MAT_BuC = self.matrixer(B_array+C_array, src_index)
        MAT_AuC = self.matrixer(A_array+C_array, src_index)

        print "MAT_BuC", MAT_BuC
        print "MAT_AuC", MAT_AuC

        print "- Get Transposed mats -"
        print "Transposed MAT_BuC", MAT_BuC.T
        print "Transposed MAT_AuC", MAT_AuC.T

        orthogonal_BuC = A_matrix.dot(MAT_BuC.T)
        orthogonal_AuC = B_matrix.dot(MAT_AuC.T)

        print "Orthogonal BuC: ", orthogonal_BuC
        print "Orthogonal AuC: ", orthogonal_AuC

        orthogonal_sum = orthogonal_BuC + orthogonal_AuC
        print "SUM?", orthogonal_sum

        """
        orthogonal_vectors = self.rpf_class.get_orthogonal_vectors(None, 3)
        """

        def get_orthogonal_indexes(lengths, orthogonal_sum):

            print "ORTHOGONAL SUM", orthogonal_sum
            print "LENGTHS", lengths

            #print "ranger row", range(0, lengths[0])
            #print "ranger i", range(0, lengths[0])
            #print "ranger j", range(lengths[0], lengths[1]+lengths[2])
            for row in range(0, lengths[0]):
                print "ROW in A_matrix", row
                for i in range(0, lengths[0]):
                    print "1.i - orthogonal_sum[row, i]", i, "-", orthogonal_sum[row, i]
                    if orthogonal_sum[row, i] == 0:
                        for j in range(lengths[0], lengths[1]+lengths[2]):
                            print "2. j - orthogonal_sum[row, j]", j, "-", orthogonal_sum[row, j]
                            if orthogonal_sum[row, j] == 0:
                                print "I, J, ROW", i, j, row
                                j = j-(lengths[1])
                                print "subbed J", j
                                return i, j, row
            #print "I,J ROW", i, j, row
            raise Exception("Failed")

        i, j, row = get_orthogonal_indexes(lengths, orthogonal_sum)

        orthogonal_vectors = list()

        orthogonal_vectors.append(A_array[row].tolist())
        orthogonal_vectors.append(B_array[i].tolist())
        orthogonal_vectors.append(C_array[j].tolist())

        print "orthogonal_vectors", orthogonal_vectors

        dpid_paths = list()

        for vector in orthogonal_vectors:
            #vector.insert(0, 1)

            dpid_row = list()
            pos = 0
            for item in vector:
                if item == 1:
                    print "vindex", pos
                    print "item", item, vector
                    item_dpid = dpids.keys()[pos]
                    print "item_dpid", item_dpid
                    dpid_row.append(item_dpid)
                pos += 1

            dpid_paths.append(dpid_row)
            print "current_conn_row_list", dpid_paths


        print "dpid_paths", dpid_paths

        return dpid_paths


####################################################################
def launch():
    global start_time
    start_time = datetime.datetime.now()
    print "Start Time: ", start_time

    log.info(" Registering Resilient Path Finder")
    core.registerNew(ResilientModule)

    #import pox.topology
    #pox.topology.launch()
    import pox.openflow.discovery
    pox.openflow.discovery.launch()
    #import pox.openflow.topology
    #pox.openflow.topology.launch()

    #core.call_when_ready(start_method, "name")





