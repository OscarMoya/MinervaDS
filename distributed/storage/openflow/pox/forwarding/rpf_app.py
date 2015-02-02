"""
"""

from pox.core import core
from pox.host_tracker import host_tracker
from pox.lib.util import dpidToStr
from service_thread import ServiceThread
from distributed.storage.openflow.pox.forwarding.rpf import ResilientPathFinder
#TODO: import host_finder class
from distributed.storage.openflow.pox.forwarding.host_finder import host_tracker


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


config_magic_ip = DSConfig.MAGIC_IP


if pckt_in_dst_ip != config_magic_ip:
      log.warning("Couldn't find magic_ip in packet-in event packet")
      pass

if pckt_in_dst_ip not in host_list:
      log.info('Received packet-in event packet from unknown host')
      pass

class ResilientModule(object):

    def __init__(self, reactive, ignore=None):
        """
        Initialize

        See LearningSwitch for meaning of 'transparent'
        'reactive' indicates how
        'ignore' is an optional list/set of DPIDs to ignore
        """
        log.info("Initializing Resilient Path Finder")
        core.openflow.addListeners(self)
        self.reactive = reactive
        self.ignore = set(ignore) if ignore else ()

        self.topology = list()
        self.priority = 65000 #16777215 # Highest priority

        if self.reactive:
            try:
                core.openflow.addListenerByName("PacketIn", self._handle_PacketIn)
            except Exception as e:
                log.info(e)
        else:
            core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
        log.info("Network Coding Correctly Initialized")











#TODO: To implement, topology?
def main(topology, src, dst, n_flows):
    """
    Main RPF algorithm process; Needed Inputs are:
    - Network topology ()
    - End points (src and dst)
    - Number of resilience flows (tipically flows=3: A, B, AxB)
    """
    resilient = ResilientPathFinder()

    #TODO: To implement; Retrieve POX topology
    #Network topology should be retrieved from controller and parsed in next format

    dpids = {1: {2: 2, 3: 3, 4: 4, 5: 5},
            2: {1: 1, 3: 3, 4: 4, 5: 5},
            3: {1: 1, 2: 2, 4: 4, 5: 5},
            4: {1: 1, 2: 2, 3: 3, 5: 5},
            5: {1: 1, 2: 2, 3: 3, 4: 4}, }

    arrays = list()

    for key in dpids.keys():

        conn_row = dpids[key].keys()
        conn_row.sort()
        conn_row_array = numpy.array(conn_row)
        conn_row_array = conn_row_array/conn_row_array
        conn_row = conn_row_array.tolist()
        conn_row.insert((key-1), 0)
        arrays.append(numpy.array(conn_row))

    #TODO: Convert topology to numpy.matrix (def method():)
    #Retrieved topology must be converted into numpy.arrays -> numpy.matrix

    a2 = numpy.array([0, 1, 1, 0])
    b2 = numpy.array([1, 0, 0, 1])
    c2 = numpy.array([1, 0, 0, 1])
    d2 = numpy.array([0, 1, 1, 0])
    #e2 = numpy.array([1, 1, 1, 1, 0])

    #matrix2 = numpy.matrix([a2,b2,c2,d2,e2,f2,g2])
    matrix2 = numpy.matrix([a2, b2, c2, d2])
    src_dpid2 = 1
    dst_dpid2 = 4
    #dst_dpid2 = 7

    result = resilient.get_potential_paths(src_dpid2, dst_dpid2, matrix2)
    final = list()

    for r in result:
        if type(r[0]) == list:
            continue
        final.append(r)

    flows = resilient.flows

    print "final:", final
    len3 = list()
    for i in final:
        if len(i) == 3:
            len3.append(i)
    print len3

    import pprint

    array_list = list()
    for i in final:
        array_list.append(resilient.generate_adjacency_vector(i, 4))

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

    final_result = list
    orthogonal_vectors = resilient.get_orthogonal_vectors(mat, 3)
    splitter, merger = resilient.find_places_for_nfs(orthogonal_vectors, 3)

    if splitter and not merger:
        merger = 4
    elif not splitter and not merger:
        merger = 4
        splitter = 1

    for ov in orthogonal_vectors:
        ov.insert(0, src_dpid2)
        ov.append(dst_dpid2)

    #TODO: Check first print, incorrect var
    if len(orthogonal_vectors) == flows:
        print "The computated result was that the paths to be taken are: ", paths
    else:
        print "Not enough resilient paths calculated, there should be a splitter on node %d and a merger on %d" %(splitter, merger)

    print "ORTHOGONAL_VECTORS: ", orthogonal_vectors


################################################
"""
if __name__ == "__main__":
    main(None, None, None, None)
"""

def launch():
    global start_time
    start_time = datetime.datetime.now()
    print "Start Time: ", start_time

    log.info("Registering Resilient Path Finder")
    core.registerNew(ResilientPathFinder)

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
"""




