import os, math
import numpy as np
from collections import namedtuple

Customer = namedtuple("Customer", ['index',  'x', 'y', 'demand', 'start', 'end', 'service'])
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
        info = dict()

        for i, line in enumerate(my_filelines):
            if line.startswith("VEHICLE"):
                vehicle_pro_start = i + 2
            elif line.startswith("CUSTOMER"):
                customer_pro_start = i + 3

            elif line.startswith("NUMBER"):
                splited = line.split(' ')
                info[splited[0]] = 0
                info[splited[-1]] = 0
        return info, (vehicle_pro_start, customer_pro_start)


    def _return_node_lists(self, my_breaklines):
        """
        read the node demand and coordinates information
        """
        my_filelines = self.file_lines
        v_start, c_start = my_breaklines

        for i, line in enumerate(my_filelines):
            if v_start == i:
                vehicle_part = line.strip().split(' ')
                self.info['NUMBER'], self.info['CAPACITY'] = int(vehicle_part[0]), int(vehicle_part[-1])
            if c_start <= i:
                c_part = line.strip().split(' ')
                c_store = list()
                for j in c_part:
                    try:
                        c_store.append(int(j))

                    except ValueError:
                        continue
                if c_store != []:
                    self.customers.append(
                        Customer(c_store[0], c_store[1], c_store[2], c_store[3], c_store[4], c_store[5], c_store[6]))


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
                    self.distance_matrix[i][j] = round(distance)


def init_data(filename):
    #the data file
    raw_data = Importer()
    raw_data.import_data(filename)
    # customers (include the depot)
    depot = raw_data.customers[0]
    customers = raw_data.customers[1:]
    # demand list, coordinates list
    demand_list = list()
    coordinates = list()
    for i in raw_data.customers:
        demand_list.append(i.demand)
        coordinates.append((i.x, i.y))
    # vehicle capacity
    vehicle_capacity = int(raw_data.info["CAPACITY"])
    # distance
    distance_matrix = raw_data.distance_matrix
    return customers, depot, demand_list, vehicle_capacity, coordinates, distance_matrix


if __name__ == '__main__':
    file_name = os.path.join(BASE_DIR, 'data\Solomon_25\C101.25.txt')
    customers, depot, demand_list, vehicle_capacity, coordinates, distance_matrix = init_data(file_name)

