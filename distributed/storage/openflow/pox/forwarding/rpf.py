"""
MINERVA - RPF for POX Controller
Resilient Path Finder
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
from service_thread import ServiceThread
import os
import datetime
import time
import traceback
import numpy
import copy

class ResilientPathFinder():

    def __init__(self, n_flows=None):
        if n_flows == None:
            self.flows = 3
        else:
            self.flows = n_flows

    def get_potential_paths(self, src_dpid, dst_dpid, matrix, path=list(), result=list()):
        """
        Find all those candidate paths that might have a resilient path from source to destination
        Old get_resilient_path
        """
        current_path = copy.deepcopy(path)
        current_path.append(dst_dpid)

        print "..............................dst_dpid", dst_dpid
        print "..............................src_dpid", src_dpid

        if dst_dpid == src_dpid:
            print "dst_dpid == src_dpid"
            return current_path

        if matrix.max() == 0:
            print "matrix.max() == 0"
            return None

        dst_array = self.__get_dpid_array(dst_dpid, len(matrix))
        print "dst_array", dst_array
        neo_matrix = copy.deepcopy(matrix)
        print "neo_matrix", neo_matrix
        neo_matrix[dst_dpid - 1].fill(0)
        candidates = self.__get_candidates_to_dst(dst_array, matrix)
        print "candidates", candidates

        for candidate in candidates:
            print "candidate - candidates", candidate, "-", candidates
            print "self.get_potential_paths(src_dpid, candidate)", src_dpid, candidate
            circuit = self.get_potential_paths(src_dpid, candidate, neo_matrix, current_path)
            if circuit:
                print "circuit", circuit
                result.append(circuit)

        return result

    def __get_dpid_array(self, dpid_num, length):
        dpid = list("0" * length)
        dpid_array = numpy.array(dpid, dtype=int)
        dpid_array.put(dpid_num - 1, 1)
        return dpid_array

    def __get_candidates_to_dst(self, dst, matrix):

        #TODO:
        result = (matrix * numpy.matrix(numpy.matrix(dst)).T).T     #Formats the matrix as list
        candidates = list()
        i = 0

        for value in result.tolist()[0]:     #In numpy notation
            if value == 1:
                candidates.append(i + 1)
            i += 1

        return candidates

    def find_places_for_nfs(self, resilient_paths, n_flows, used_nodes=list()):
        required_nf_pairs = n_flows - len(resilient_paths)
        print "required_nf_pairs", required_nf_pairs

        if required_nf_pairs == 0:
            return None, None

        all_nodes = list()
        r_paths = copy.deepcopy(resilient_paths)

        for r in r_paths:
            all_nodes.extend(r)
        candidates = list()

        for r in all_nodes:
           i = all_nodes.count(r)
           if i >= 2 and r not in candidates and r not in used_nodes:
               candidates.append(r)

        if len(candidates) >= 2:
            return min(candidates), max(candidates)

        elif len(candidates) == 1:
            return candidates[0]

        else:
            return None

    def generate_adjacency_vector(self, array, length):
        empty_array = list("0" * length)
        adj_array = numpy.array(empty_array, dtype=int)

        for i in array:
            adj_array.put(i-1, 1)

        return adj_array.tolist()

    def get_orthogonal_vectors(self, mat, n_flows):
        print "- Get Orthogonal Vectors Method -"
        print "Init Mat: ", mat
        orthogonal_map = mat.dot(mat.T)
        orthogonal_vector_list = list()
        print "Orthogonal map: ", orthogonal_map
        orthogonal_map = orthogonal_map.T       #Transposed for easy vector indexing
        print "ORTHOGONAL MAP Transposed: ", orthogonal_map

        for row in orthogonal_map:
            if row.sum() == 0:
                orthogonal_vector_list.append(-1)       #zeroed vectors must be treated specially
                continue

            orthogonal_vector_list.append(row.tolist()[0].count(0))

        print "ORTHOGONAL_VECTOR_LIST: ", orthogonal_vector_list
        max_orthogonal_vectors = max(orthogonal_vector_list)
        best_row = orthogonal_map[orthogonal_vector_list.index(max_orthogonal_vectors)]
        src_vector = orthogonal_vector_list.index(max_orthogonal_vectors)
        print "BEST_ROW: ", best_row
        indexes = list()
        best_row = best_row.tolist()[0]

        for i in range(0, len(best_row)):
            if best_row[i] == 0:
                indexes.append(i)

        indexes.insert(src_vector,src_vector)
        result = list()
        print "Indexes: ", indexes

        for i in indexes:
           result.append(mat[i].tolist()[0])

        return result[0:n_flows]