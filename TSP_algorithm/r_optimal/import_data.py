#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/17 7:57
# import tsp data

import os
import numpy
from collections import deque

BASE_DIR = os.path.abspath('.')


class Importer(object):
    '''Read the meta data from the file'''

    def __init__(self):
        self.file_lines = []
        self.info = {}
        self.city_coordinates_list = []
        self.distance_matrix = None
        self.city_num = None

    def import_data(self, filename):
        self._read_file(filename)
        self.info, part_mark, end_mark = self._read_info()
        self.city_coordinates_list = self._return_city_coordinate(part_mark, end_mark)
        self.city_num = len(self.city_coordinates_list)
        adjacency_matrix_list = \
            self._create_distance_matrix(self.city_coordinates_list, int(self.info["DIMENSION"]))
        self.distance_matrix = numpy.array(adjacency_matrix_list)

    def _read_file(self, my_filename):
        file_lines = []
        with open(my_filename, "rt") as f:
            file_lines = f.read().splitlines()
        self.file_lines = file_lines

    def _read_info(self):
        """
        read the data file information
        :return:
        """
        my_filelines = self.file_lines
        info = {}
        part_mark = 0
        for i, line in enumerate(my_filelines):
            if line.startswith("NODE_COORD_SECTION"):
                part_mark = i
            elif line.startswith("EOF"):
                end_mark = i
            elif line.split(' ')[0].isupper():  # checks if line begins with UPPERCASE key
                splited = line.split(':')
                info[splited[0].strip()] = splited[1].strip()
        return info, part_mark, end_mark

    def _return_city_coordinate(self, part, end):
        """
        read the city coordinates
        :param park_mark:
        :return:
        """
        node_coordinates_list = []
        for i, line in enumerate(self.file_lines):
            if part < i < end:
                splited = line.strip().split(' ')
                splited = list(map(float, splited))
                node_coordinates_list.append((splited[1], splited[2]))
        return node_coordinates_list


    def _euclidian_distance(self, my_node1, my_node2):
        x1, y1 = my_node1
        x2, y2 = my_node2

        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
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
    # the data file
    raw_data = Importer()
    raw_data.import_data(filename)
    # city number
    city_number = raw_data.city_num
    # coordinates
    coordinates = raw_data.city_coordinates_list
    # distance and fitness
    distance_matrix = raw_data.distance_matrix

    return coordinates, distance_matrix, city_number


if __name__ == '__main__':
    file_name = os.path.join(BASE_DIR, 'eil51.tsp')
    coordinates, distance_matrix, city_number = init_data(file_name)

