import os
import numpy as np
from collections import namedtuple

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])
BASE_DIR = os.path.abspath('.')


class Importer(object):
    """
    Read the meta data from the file
    """
    def __init__(self):
        self.file_lines = list()
        self.info = {}
        self.coordinates = list()
        self.demand_list = list()
        self.distance_matrix = None
        self.customers = list()

    def import_data(self, filename):
        self._read_file(filename)
        self.info, break_lines = self._read_info()
        self._return_node_lists(break_lines)
        self._cal_distance_matrix()

    def _read_file(self, my_filename):
        file_lines = []
        with open(my_filename, "rt") as f:
            file_lines = f.read().splitlines()
        self.file_lines = file_lines

    def _read_info(self):
        """
        The data information vehicle count, capacity ...
        """
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

    def _return_node_lists(self, my_breaklines):
        """
        read the node demand and coordinates information
        """
        my_filelines = self.file_lines
        start, middle, end = my_breaklines

        for i, line in enumerate(my_filelines):
            if start < i < middle:
                coordinate_part = line.strip().split(' ')
                coordinate_part = list(map(float, coordinate_part))
                self.coordinates.append((coordinate_part[1], coordinate_part[2]))

            if middle < i < end:
                demand_part = line.split(' ')
                demand_part = demand_part[:2]
                demand_part = list(map(int, demand_part))
                self.demand_list.append(demand_part[1])
        i = 0
        for coord, demand in zip(self.coordinates, self.demand_list):
            self.customers.append(Customer(i, demand, coord[0], coord[1]))
            i += 1

    def _cal_distance_matrix(self):
        """
        distance matrix
        """
        customer_count = len(self.customers)
        self.distance_matrix = np.zeros([customer_count, customer_count])
        for i in range(customer_count):
            for j in range(customer_count):
                if i == j:
                    continue
                else:
                    distance = np.sqrt(np.square(self.customers[i].x - self.customers[j].x) +
                                       np.square(self.customers[i].y - self.customers[j].y))
                    self.distance_matrix[i][j] = distance


def init_data(filename):
    #the data file
    raw_data = Importer()
    raw_data.import_data(filename)
    # customers (include the depot)
    depot = raw_data.customers[0]
    customers = raw_data.customers[1:]
    # demand list
    demand_list = list()
    for i in raw_data.customers:
        demand_list.append(i.demand)
    # vehicle number
    instance_name = raw_data.info["NAME"]
    vehicle_count = int(instance_name[instance_name.rfind('k')+1:])
    # vehicle capacity
    vehicle_capacity = int(raw_data.info["CAPACITY"])
    # coordination
    coordinates = raw_data.coordinates
    # distance and fitness
    distance_matrix = raw_data.distance_matrix
    return customers, depot, demand_list, vehicle_count, vehicle_capacity, coordinates, distance_matrix


if __name__ == '__main__':
    file_name = os.path.join(BASE_DIR, 'data\A-n32-k5.vrp') 
    customers, depot, demand_list, vehicle_count, vehicle_capacity, coordinates, distance_matrix = init_data(file_name)

