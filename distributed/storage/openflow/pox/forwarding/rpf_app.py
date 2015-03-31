"""
"""
from pox.core import core
from pox.forwarding.rpf import ResilientPathFinder
from pox.forwarding.host_finder import Hostfinder
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
            #self.cl_magic_ip = DSConfig.MAGIC_IP
            #self.sv_magic_ip = DSConfig.MAGIC_IP
            self.cl_magic_ip = "10.10.100.254"
            self.sv_magic_ip = "10.10.100.253"
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
                dpid = host.dpid
                return dpid
        return dpid

    def compare_dpid(self, dpid_list):
        if len(set(dpid_list)) == 1:
            return True
        else:
            return False

    def match_host_type(self, ip):
        for host in self.host_finder.hosts:
            if host.ip == ip and host.type == 'client':
                return Match("client")
            elif host.ip == ip and host.type == 'server':
                return Match("server")
        
        raise Exception("No match available")    

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
        log.info("PacketIn Correctly Parsed")
        
        if eth_headers.next.id != 1550:
            return

        dpid = event.dpid
        in_port = event.port  

        if eth_headers.next.eth_type == 2054 or eth_headers.next.eth_type == 2048:     # ARP datagram type hex 0806; 2054
            
            if eth_headers.next.eth_type == 2048:
                ip_params = eth_headers.next.next
                src_mac = eth_headers.src      # ETHER_ANY
                dst_mac = eth_headers.dst      # ETHER_ANY
                src_ip = ip_params.srcip       # IP_ANY
                dst_ip = ip_params.dstip
            else:
                arp_params = eth_headers.next.next
                src_mac = arp_params.hwsrc      # ETHER_ANY
                dst_mac = arp_params.hwdst      # ETHER_ANY
                src_ip = arp_params.protosrc   # IP_ANY
                dst_ip = arp_params.protodst

            if dst_ip == self.cl_magic_ip or dst_ip == self.sv_magic_ip:
                found = self.host_search(src_ip)

                if not found:
                    log.info(' --> Received packet-in event packet from unknown host')
                   
                    if dst_ip == self.cl_magic_ip:
                        self.host_finder.add_host(src_ip, src_mac, dpid, in_port, 'client')
                    elif dst_ip == self.sv_magic_ip:
                        self.host_finder.add_host(src_ip, src_mac, dpid, in_port, 'server')
                else:
                    log.info(' --> Received packet-in event packet from already known host')

            else:   # dst_ip != self.magic_ip:
                log.info(" Packet-in event packet with no magic-ip")

                packet_match = self.match_host_type(src_ip)
               
                if packet_match.match_type == "client":
                    packet_match.in_port = in_port
                    packet_match.src_mac = src_mac
                    packet_match.dst_mac = dst_mac
                    packet_match.vlan_id = None
                    packet_match.vlan_priority = None
                    packet_match.src_ip = src_ip
                    packet_match.dst_ip = dst_ip
                    packet_match.ip_tos = None
                    packet_match.l3_src_port = None
                    packet_match.l3_dst_port = None

                else:
                    packet_match.vlan_id = 1550
                    packet_match.src_ip = dst_ip
                    packet_match.dst_ip = src_ip

                log.info(" --> New packet_match")

                self.packet_holder.check_in(packet_match)
                pkt_ready = self.packet_holder.take_off() #list of lists
                self.host_finder.update_topology()
                matrix = self.host_finder.topology_to_matrix()

                # Get src and dst dpids, select RPF type
                if pkt_ready:
                    dsts_ip = list()
                    pkt_root = pkt_ready[0][0].get_root()
                    in_port = pkt_root.get_in_port()
                    src_mac = pkt_root.get_src_mac()
                    eth_type = pkt_root.get_eth_type()
                    vlan_id = pkt_root.get_vlan_id()
                    srcs_ip = pkt_root.get_src_ip()

                    for dsts in pkt_ready:
                        for match_item in dsts:
                            print mcolors.OKGREEN+"-PACKET_MATCH READY-"+mcolors.ENDC
                            dsts_ip.append(match_item.get_dst_ip())

                    if type(dsts_ip) is list:

                        dpid_src = self.get_dpid(srcs_ip)
                        if not dpid_src:
                            log.warning(mcolors.FAIL+" Couldn't find source DPID!"+mcolors.ENDC)
                            return

                        dsts_list = list()
                        dsts_dict = dict()
                        for dsts in dsts_ip:
                            dsts_dpid = self.get_dpid(dsts)
                            if not dsts_dpid:
                                log.warning(mcolors.FAIL+" Couldn't find destination DPID!"+mcolors.ENDC)
                                return
                            else:
                                dsts_list.append(dsts_dpid)
                                dsts_dict[dsts] = dsts_dpid

                        location = self.compare_dpid(dsts_list)

                        if location:
                            # Call single_RPF(topology, src_ip, dst_ip, 3)
                            result = self.single_rpf(matrix, dpid_src, dsts_list[0], 3)
                            self.route_flows(result, packet_match, srcs_ip, dsts_ip, vlan_id=None, event=None)

                        else:
                            import threading
                            result_list = list()
                            with threading.Lock():
                                res = self.single_rpf(matrix, dpid_src, dsts_dict[dsts_ip[0]], 3)
                            result_list.append(res)
                            with threading.Lock():
                                res = self.single_rpf(matrix, dpid_src, dsts_dict[dsts_ip[1]], 3)

                            result_list.append(res)
                            with threading.Lock():
                                res = self.single_rpf(matrix, dpid_src, dsts_dict[dsts_ip[2]], 3)

                            result_list.append(res)
                            print mcolors.OKGREEN+"-MULTI-RPF starting...-"+mcolors.ENDC
                            final_result_list = self.multi_rpf(result_list, matrix, dpid_src, None)

                            self.route_flows(final_result_list, packet_match, srcs_ip, dsts_ip, vlan_id=None, event=None)

            print mcolors.OKGREEN+"-DONE-"+mcolors.ENDC

        elif eth_headers != pkt.ethernet.LLDP_TYPE:     # packet.type != ARP and LLDP
            pass
        return

    def pos_mapper(self, all_dpids, src, dst):
        pos = 1
        pos_map = dict()
        pos_rmap = dict()
        pos_map, pos_rmap = self.dict_mapper(1, src, pos_map, pos_rmap)
        all_dpids.remove(src)
        pos += 1

	if src == dst:
            return pos_map, pos_rmap

        while all_dpids:
            for dpid in all_dpids:
                if dpid == src:
                    continue
                elif dpid == dst:
                    continue
                else:
                    pos_map, pos_rmap = self.dict_mapper(pos, dpid, pos_map, pos_rmap)
                    all_dpids.remove(dpid)
                    pos += 1

            if len(all_dpids) == 1:     
                if all_dpids.index(dst) == 0:
                    last = all_dpids.pop()
                    pos_map, pos_rmap = self.dict_mapper(pos, last, pos_map, pos_rmap)

        del all_dpids
        return pos_map, pos_rmap

    def dict_mapper(self, position, dpid, mapping=dict(), rmapping=dict()):
        mapping.update({position: dpid})
        rmapping.update({dpid: position})

        return mapping, rmapping

    def pos_to_dpid(self, paths, mapping):
        '''
        Translates the connected DPIDs to its proper DPID number
        '''

        for path in paths:
            k = 1
            for index, node in enumerate(path):
                if node == 1:
                    dpid = mapping.get(k)
                    path[index] = dpid
                    k += 1
                else:
                    k += 1
                    continue
            while 0 in path:
                path.remove(0)
        return paths

    def route_flows(self, paths, matching, src_ip=None, dsts_ip=None, vlan_id=None, event=None):
        '''
        Adds the required rules to the switch flow table:
        (final_result_list, packet_match, srcs_ip, dsts_ip)
        '''

        print mcolors.FAIL+"-ROUTE_FLOWS starting...-"+mcolors.ENDC

        src_dpid, src_port = self.get_host_port(src_ip)
        links = core.openflow_discovery.adjacency.keys()

        i = 0
        for path in paths:
            if len(path) == 1:
                pass # TODO: One switch path           

            else:
                dst_dpid, dst_port = self.get_host_port(dsts_ip[i])
            	for dpid in path:
                    if dpid == src_dpid:  # First switch after src
                        try:                       
                            next_dpid = path[path.index(dpid)+1]
                        except:
                            next_dpid = path[path.index(dpid)-1]

                        for link in links:
                            if (link.dpid1 == dpid and link.dpid2 == next_dpid):
                                self.push_flow(link.dpid1, src_ip, dsts_ip[i], src_port, link.port1, None, None)
                                break
                    elif dpid == dst_dpid:     #last switch before dst
                        for link in links:
                            if (link.dpid1 == path[(path.index(dpid))-1] and link.dpid2 == dpid):
                                dst_dpid, dst_port = self.get_host_port(dsts_ip[i])
                                if dst_dpid == link.dpid2:
                                    self.push_flow(link.dpid2, src_ip, dsts_ip[i], link.port2, dst_port, None, None)
                                    break
                    else:
                        try:
                            next_dpid = path[path.index(dpid)+1]
                            pre_dpid = path[path.index(dpid)-1]
                            for linkx in links:
                                if (linkx.dpid1 == pre_dpid and linkx.dpid2 == dpid):
                                    pre_port = linkx.port2
                                    for linky in links:
                                        if (linky.dpid1 == dpid and linky.dpid2 == next_dpid):
                                            self.push_flow(linky.dpid1, src_ip, dsts_ip[i], pre_port, linky.port1, None, None)
                                            break
                                    break
                        except:
                            break
                i += 1
        return

    def push_flow(self, dpid_conn, src_ip, dst_ip, in_port, out_port, vlan_id=None, event=None):

        # Half round trip: TYPE_ETHERNET
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match(in_port=in_port,
                                 dl_type=0x0800,
                                 nw_src=src_ip,
                                 nw_dst=dst_ip)

        # Use idle and/or hard timeouts to help cleaning the table
        msg.idle_timeout = 10
        msg.hard_timeout = 0  #In order to avoid unnecessary messages between the switches and the controller
        msg.priority = 40
        msg.actions.append(of.ofp_action_output(port=out_port))

        connection = self.conn_dpids[dpid_conn]
        connection.send(msg)

        # way back trip: TYPE_ETHERNET
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match(in_port=out_port,
                                 dl_type=0x0800,
                                 nw_src=dst_ip,
                                 nw_dst=src_ip)

        # Use idle and/or hard timeouts to help cleaning the table
        msg.idle_timeout = 10
        msg.hard_timeout = 0
        msg.priority = 40
        msg.actions.append(of.ofp_action_output(port=in_port))

        connection = self.conn_dpids[dpid_conn]
        connection.send(msg)

        # half round trip: TYPE_ARP
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match(in_port=in_port,
                                 dl_type=0x0806,
                                 nw_src=src_ip,
                                 nw_dst=dst_ip)

        msg.idle_timeout = 10
        msg.hard_timeout = 0
        msg.priority = 40
        msg.actions.append(of.ofp_action_output(port=out_port))

        connection = self.conn_dpids[dpid_conn]
        connection.send(msg)

        # way back trip: TYPE_ARP
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match(in_port=out_port,
                                 dl_type=0x0806,
                                 nw_src=dst_ip,
                                 nw_dst=src_ip)

        msg.idle_timeout = 10
        msg.hard_timeout = 0
        msg.priority = 40
        msg.actions.append(of.ofp_action_output(port=in_port))

        connection = self.conn_dpids[dpid_conn]
        connection.send(msg)

    def paths_length(self, paths):
        lens_list = list()
        for path_set in paths:
            lens_list.append(len(path_set))

        return lens_list

    def paths_to_arrays(self, paths, dpids):
        # Translate all paths to 0-1 format following a common pattern
        all_dpids = self.host_finder.get_dpids()
        pos = 0

        for path_set in paths:
            arrays = list()

            for path in path_set:
                conn_row = path
                not_conn = list(set(all_dpids)-set(conn_row))
                conn_row_array = numpy.array(conn_row)
                conn_row_array = conn_row_array/conn_row_array
                conn_row_list = conn_row_array.tolist()
                # ITEMS in difference:
                for item in not_conn:
                    item_pos = dpids.keys().index(item)
                    # Add '0' in place of no dpid link
                    conn_row_list.insert(item_pos, 0)
                arrays.append(numpy.array(conn_row_list))
            pos += 1

            if pos == 1:
                A_arrays = arrays
            elif pos == 2:
                B_arrays = arrays
            elif pos == 3:
                C_arrays = arrays

        return A_arrays, B_arrays, C_arrays

    def matrixer(self, arrays, index):
        matrix_array = numpy.matrix(arrays)
        path_row_list = list()
        for a in arrays:
            row = a.tolist()
            path_row_list.append(row)
        final = list()

        for r in path_row_list:
            if type(r[0]) == list:
                continue
            final.append(r)
        flows = self.rpf_class.flows

        len3 = list()
        for i in final:
            if len(i) == 3:
                len3.append(i)

        import pprint
        array_list = list()

        # Delete all srcs for each mat row
        import pprint

        # Delete only the src column and delete possible repeated vectors:
        array_list_2 = list()
 
        for i in final:
            nw_list = list()
            pos = 0
            for j in i:
                if pos != index:
                    nw_list.append(j)
                    pos += 1
                else:
                    pos += 1

            array_list_2.append(nw_list)
           
        mat = numpy.matrix(array_list_2)
        return mat   

        # Creating matrix

        mat = numpy.matrix(final)
        return mat

    def single_rpf(self,  dpids, src, dst, n_flows=None):
        """
        Main RPF algorithm process for single location of servers (same dst_dpid); Needed Inputs are:
        - Network topology ()
        - End points (src and dst)
        - Number of resilience flows (current flows=3: A, B, AxB)
        """

        # Network topology should be retrieved from controller and parsed in next format
        arrays = list()
        all_dpids = self.host_finder.get_dpids()
        pos_dpid_map, dpid_pos_map = self.pos_mapper(all_dpids, src, dst)
        # Network topology should be retrieved from controller and parsed in next format

        """
        dpids = {1: {2: 2, 3: 3, 4: 4, 5: 5},
                2: {1: 1, 3: 3, 4: 4, 5: 5},
                3: {1: 1, 2: 2, 4: 4, 5: 5},
                4: {1: 1, 2: 2, 3: 3, 5: 5},
                5: {1: 1, 2: 2, 3: 3, 4: 4},}
        """

        all_dpids_cp = pos_dpid_map.keys()
        num_dpids = len(all_dpids_cp)
        dpid_keys = pos_dpid_map.values()
        for key in dpid_keys:
            conn_row = dpids[key].keys()
            for item in conn_row:
                replace = dpid_pos_map.get(item)
                oldindex = conn_row.index(item)
                conn_row.insert(oldindex, replace)
                conn_row.pop(conn_row.index(item))           
            not_conn = list(set(all_dpids_cp)-set(conn_row))
            conn_row_len = len(conn_row)
            conn_row_array = numpy.array(conn_row)
            conn_row_array = conn_row_array/conn_row_array
            conn_row_list = conn_row_array.tolist()

            # Check key (dpid)
            # For items in difference: if item != key:
            for item in not_conn:
                # get position from pos_dpid_map
                #item_pos = pos_dpid_map.values().index(item)
                item_pos = item - 1
                # Add '0' in place of no dpid link
                conn_row_list.insert(item_pos, 0)
            arrays.append(numpy.array(conn_row_list))

        # Retrieved topology must be converted into numpy.arrays -> numpy.matrix

        matrix_array = numpy.matrix(arrays)
        result = self.rpf_class.get_potential_paths(1, len(all_dpids_cp), matrix_array)
        final = list()

        for r in result:
            if type(r[0]) == list:
                continue
            final.append(r)

        flows = self.rpf_class.flows

        len3 = list()
        for i in final:
            if len(i) == 3:
                len3.append(i)

        import pprint

        array_list = list()
        for i in final:
            array_list.append(self.rpf_class.generate_adjacency_vector(i, len(all_dpids_cp)))

        array_list_2 = list()

        for i in array_list:
            while array_list.count(i) > 1:
                array_list.remove(i)

        for i in array_list:
            array_list_2.append(i[1:len(i)-1])

        mat = numpy.matrix(array_list_2)

        final_result = list()
        orthogonal_vectors = self.rpf_class.get_orthogonal_vectors(mat, 3)
        splitter, merger = self.rpf_class.find_places_for_nfs(orthogonal_vectors, 3)

        if splitter and not merger:
            merger = len(all_dpids_cp)
        elif not splitter and not merger:
            merger = len(all_dpids_cp)
            splitter = 1

        for ov in orthogonal_vectors:
            ov.insert(0, 1)     #ov.insert(0, src_dpid2)
            ov.append(1)        #ov.append(dst_dpid2)

        if len(orthogonal_vectors) == flows:
            print "The computated result enables resilient paths to be taken" # orthogonal_vectors  #paths
        else:
            print "Not enough resilient paths calculated, there should be a splitter on node %d and a merger on %d" %(splitter, merger)

        dpid_paths = self.pos_to_dpid(orthogonal_vectors, pos_dpid_map)
        pos_dpid_map = {}
        return dpid_paths

    def multi_rpf(self, paths, dpids, src, dst):
        """
        Second RPF algorithm process for multiple location of servers(different dst_dpid); Needed Inputs are:
        - Resilient paths
        - Network topology ()
        - End points (src and (dsts))
        """
        src_index = dpids.keys().index(src)
        A_array, B_array, C_array = self.paths_to_arrays(paths, dpids)
        lengths = self.paths_length(paths)

        # Create matrixes
        A_matrix = self.matrixer(A_array, src_index)
        B_matrix = self.matrixer(B_array, src_index)
        C_matrix = self.matrixer(C_array, src_index)

        MAT_BuC = self.matrixer(B_array+C_array, src_index)
        MAT_AuC = self.matrixer(A_array+C_array, src_index)

        orthogonal_BuC = A_matrix * (MAT_BuC.T)
        orthogonal_AuC = B_matrix * (MAT_AuC.T)

        orthogonal_sum = orthogonal_BuC + orthogonal_AuC

        def get_orthogonal_indexes(lengths, orthogonal_sum):
            for row in range(0, lengths[0]):
                for i in range(0, lengths[0]):
                    if orthogonal_sum[row, i] == 0:
                        for j in range(lengths[0], lengths[1]+lengths[2]):
                            if orthogonal_sum[row, j] == 0:
                                j = j-(lengths[1])
                                return i, j, row
            raise Exception("Failed")

        i, j, row = get_orthogonal_indexes(lengths, orthogonal_sum)

        orthogonal_vectors = list()
        orthogonal_vectors.append(A_array[row].tolist())
        orthogonal_vectors.append(B_array[i].tolist())
        orthogonal_vectors.append(C_array[j].tolist())

        dpid_paths = list()

        for vector in orthogonal_vectors:
            dpid_row = list()
            pos = 0
            for item in vector:
                if item == 1:
                    item_dpid = dpids.keys()[pos]
                    dpid_row.append(item_dpid)
                pos += 1
            dpid_paths.append(dpid_row)
        return dpid_paths


def launch():
    global start_time
    start_time = datetime.datetime.now()
    print "Start Time: ", start_time

    log.info(" Registering Resilient Path Finder")
    core.registerNew(ResilientModule)

    import pox.openflow.discovery
    pox.openflow.discovery.launch()
