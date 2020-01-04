#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/16 6:51
# Description: import the vrp data


import os
import numpy
from collections import deque
BASE_DIR = os.path.abspath('.')


class Importer(object):
    '''Read the meta data from the file'''
    def __init__(self):
        self.file_lines = []
        self.info = {}
        self.node_coordinates_list = []
        self.distance_matrix = None
        self.demand_array = None
        self.depot = []
        self.depot_num = None
        self.customer_num = None

    def import_data(self, filename):
        self._read_file(filename)
        self.info, break_lines = self._read_info()
        self.node_coordinates_list, demand_list = \
            self._return_nodes_and_delivery_lists(break_lines)
        self.node_num = len(self.node_coordinates_list)
        # depot position
        depot_coordinates = self.node_coordinates_list[-1]
        self.node_coordinates_list.pop(-1)
        self.node_coordinates_list.insert(0, depot_coordinates)
        # demand list
        depot_demand = demand_list[-1]
        demand_list.pop(-1)
        demand_list.insert(0, depot_demand)
        adjacency_matrix_list = \
            self._create_distance_matrix(self.node_coordinates_list, int(self.info["DIMENSION"]))
        self.distance_matrix = numpy.array(adjacency_matrix_list)
        self.demand_array = numpy.array(demand_list)

    def _read_file(self, my_filename):
        filelines = []
        with open(my_filename, "rt") as f:
            filelines = f.read().splitlines()
        self.file_lines = filelines

    def _read_info(self):

        my_filelines = self.file_lines
        info = {}
        start = 0
        middle = 0
        end = 0

        for i, line in enumerate(my_filelines):
            if line.startswith("NODE_COORD_SECTION"):
                start = i
            elif line.startswith("DEMAND_SECTION"):
                middle = i
            elif line.startswith("DEPOT_SECTION"):
                end = i
            elif line.startswith("EOF"):
                break
            elif line.split(' ')[0].isupper():  # checks if line begins with UPPERCASE key
                splited = line.split(':')
                info[splited[0].strip()] = splited[1].strip()
            
        return info, (start, middle, end)

    def _return_nodes_and_delivery_lists(self, my_breaklines):
        my_filelines = self.file_lines
        start, middle, end = my_breaklines
        node_coordinates_list = []
        demand_list = []
        depot = []

        for i, line in enumerate(my_filelines):
            if start < i < middle:
                splited = line.strip().split(' ')
                splited = list(map(float, splited))
                node_coordinates_list.append((splited[1], splited[2]))

            if middle < i < end:
                splited = line.split(' ')
                splited = splited[:2]
#                 print (splited) 
                splited = list(map(int, splited))
                demand_list.append(splited[1])
                
            if i > end:
                splited = line.split(' ')
                if splited[0] == 'DEPOT_SECTION':
                    break

        return node_coordinates_list, demand_list

    def _euclidian_distance(self, my_node1, my_node2):
        x1, y1 = my_node1
        x2, y2 = my_node2
    
        distance = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
        return distance

    def _create_distance_matrix(self, my_node_coordinates_list, my_dimension):
        ncl = deque(my_node_coordinates_list[:])
        matrix = []
        while ncl:
            row = [0] * (my_dimension + 1 - len(ncl))
            node1 = ncl.popleft()
            for node2 in ncl:
                row.append(self._euclidian_distance(node1, node2))
            matrix.append(row)

        for i in range(my_dimension):  # mirroring the matrix
            for j in range(my_dimension):
                try:
                    matrix[j][i] = matrix[i][j]
                except IndexError as e:
                    print("##ERROR!##\nBad indexing: " + str((i, j)))
                    print("that definitly shouldnt happen, it >might< be a problem with the imported file")
                    raise e
        return matrix


def init_data(filename):
    #the data file
    raw_data = Importer()
    raw_data.import_data(filename)
    #vehicle capacity
    vehicle_capacity = int(raw_data.info["CAPACITY"])
    #vehicle endurance
    try:
        raw_data.info["DISTANCE"]
    except KeyError:
        print('No distance constraint !')
        vehicle_endurance = float('inf')
        service_time = 0
    else:
        vehicle_endurance = float(raw_data.info["DISTANCE"])
        service_time = float(raw_data.info["SERVICE_TIME"])
    # coordinates
    coordinates = raw_data.node_coordinates_list 
    # node demand
    demand_list = raw_data.demand_array
    # distance and fitness
    distance_matrix = raw_data.distance_matrix

    return vehicle_capacity, vehicle_endurance, service_time, demand_list, coordinates, distance_matrix

if __name__ == '__main__':
    file_name = os.path.join(BASE_DIR, 'Christofides1979\CMT6.vrp')
    vehicle_capacity, vehicle_endurance, service_time, demand_list, coordinates, distance_matrix = init_data(file_name)

