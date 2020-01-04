#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/16 6:51
# Description: import the vrp data; create the initial group randomly


import os
import numpy, math, random
from collections import deque
BASE_DIR = os.path.abspath('.')


class Importer(object):
    """
    Read the meta data from the file
    """
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
        self.node_coordinates_list, demand_list, depot = \
            self._return_nodes_and_delivery_lists(break_lines)
        self.node_num = len(self.node_coordinates_list)
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
#                 print (splited)
                if splited[0] == 'EOF':
                    break
                splited = splited[1] # the data format has ' '
                
                if splited != '-1':
                    depot.append(int(splited))

        return node_coordinates_list, demand_list, depot

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
    # coordination
    coordination = raw_data.node_coordinates_list 
    # node demand
    demand_list = raw_data.demand_array
    # distance and fitness
    distance_matrix = raw_data.distance_matrix

    return vehicle_capacity, demand_list, coordination, distance_matrix


def configure_group(demand_list, vehicle_capacity, num, sorting_mark=True):
    """
    configure the group by demand sorting or randomly

    """
    demand_list = demand_list.tolist()
    node_demand = demand_list[:]
    if sorting_mark:
        node_demand.sort()  # increased
    else:
        random.shuffle(node_demand)
    group = dict()
    total_demand = 0
    group_num = 1
    for i in range(num):
        group[i+1] = list()
    for demand in node_demand[::-1]:
        if demand == 0:
            continue
        if total_demand + demand <= vehicle_capacity:
            node_id = demand_list.index(demand)
            demand_list[node_id] = 0
            total_demand += demand
            group[group_num].append(node_id)
        else:
            # new group
            group_num += 1
            if group_num > num:
                return None
            node_id = demand_list.index(demand)
            demand_list[node_id] = 0
            total_demand = demand
            group[group_num].append(demand)
    return group
    # print(group)
    # input('123')


if __name__ == '__main__':
    file_name = os.path.join(BASE_DIR, 'data\A-n32-k5.vrp') 
    vehicle_capacity, demand_list, coordination, distance_matrix = init_data(file_name)
    # --- create the random groups --- #
    least_vehicle_number = math.ceil(sum(demand_list) / vehicle_capacity)  # up to integer
    random_group_count = 10
    all_group = list()
    while random_group_count:
        if random_group_count == 10:
            group = configure_group(demand_list, vehicle_capacity, least_vehicle_number, sorting_mark=True)
            all_group.append(group)
            random_group_count -= 1
        else:
            group = configure_group(demand_list, vehicle_capacity, least_vehicle_number, sorting_mark=False)
            if group == None:
                continue
            else:
                all_group.append(group)
                random_group_count -= 1
    # print the result
    for group in all_group:
        print(group)
        nn = sum(len(i) for key, i in group.items())
        print(nn)


