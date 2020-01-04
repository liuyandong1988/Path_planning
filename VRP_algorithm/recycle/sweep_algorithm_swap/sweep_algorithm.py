#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/16 6:51
# Description: ‘A Heuristic Algorithm for the Vehicle-Dispatch Problem’ by Billy E.
#               Operations Research, Vol. 22, No. 2 (Mar. - Apr., 1974), pp. 340-349Published
#               (1) sweep algorithm
#               (2) 2-opt tsp

import import_data
import os, math
import tsp2opt
from matplotlib import pyplot as plt
import numpy as np

class Node(object):

    def __init__(self, id, coordinate, demand = 0):
        self.id = id
        self.coordinate = coordinate
        self.demand = demand
        self.polar_angle = 0
        self.radius = 0


class SweepAlgorithm(object):

    def __init__(self, vehicle_capacity, demand_list, coordinates, distance_matrix):
        self.v_capacity = vehicle_capacity
        self.c_demand = demand_list
        self.coordinates = coordinates
        self.distance_matrix = distance_matrix
        self.init_nodes()
        self.polar_sort()

    def init_nodes(self):
        """
        initial nodes
        """
        # --- depot --- #
        self.depot_list = list()
        depot_id = 0
        for i in self.coordinates[0:1]:
            self.depot_list.append(Node(depot_id, i))
            depot_id += 1
        # --- customer --- #
        self.customer_list = list()
        customer_id = depot_id
        for i, c in enumerate(self.coordinates[customer_id:]):
            self.customer_list.append(Node(customer_id, c, self.c_demand[i]))
            customer_id += 1

    def polar_sort(self):
        d_coordinate = self.coordinates[0]
        c_coordinates = self.coordinates[1:]
        node_id = 1
        self.store_info = list()
        print(len(c_coordinates))
        for ind, c_coordinate in enumerate(c_coordinates):
            angle_tmp = math.atan((c_coordinate[1]-d_coordinate[1])/(c_coordinate[0]-d_coordinate[0]))
            if c_coordinate[1]-d_coordinate[1] < 0:
                if angle_tmp > 0:
                    angle_tmp = -math.pi + angle_tmp
                else:
                    pass
            else:
                if angle_tmp > 0:
                    pass
                else:
                    angle_tmp = math.pi + angle_tmp
            radius_tmp = self.cal_distance(c_coordinate, d_coordinate)
            self.store_info.append([node_id, angle_tmp, radius_tmp])
            self.customer_list[ind].polar_angle = angle_tmp
            self.customer_list[ind].radius = radius_tmp
            node_id += 1
        # sorting increase
        self.store_info.sort(key=lambda x: x[1], reverse=False)
        # print('Sorting:', self.store_info)

    def cal_length(self, solution):
        """
        calculate the route length
        :param distance_matrix:
        :return:
        """
        total_distance = 0
        #     print solution
        for (city1, city2) in zip(solution[:-1], solution[1:]):
            total_distance += self.distance_matrix[city1][city2]
        total_distance += self.distance_matrix[solution[-1]][solution[0]]
        return total_distance

    def cal_distance(self, my_node1, my_node2):
        x1, y1 = my_node1
        x2, y2 = my_node2
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance

    def run(self):
        """
        cluster based on the polar
        :return:
        """
        tmp_capacity = 0
        route_id = 1
        route_node = list()
        all_route = dict()
        new_route_mark = False
        # --- initial routes by polar angle --- #
        while self.store_info:
            if new_route_mark:
                new_route_mark = False
            else:
                node = self.store_info.pop(0)
            overload_mark, tmp_capacity = self.constraint_capacity(tmp_capacity, self.c_demand[node[0]])

            if overload_mark:
                # generate a route
                all_route[route_id] = route_node
                # reset new route
                route_id += 1
                route_node = list()
                tmp_capacity = 0
                new_route_mark = True
            else:
                route_node.append(node[0])
        # the last route
        all_route[route_id] = route_node
        # optimal the each route by 2-opt
        result_routes = dict()
        for route_id, route in all_route.items():
            route.append(0)
            opt_route = self.tsp_2opt(route)
            result_routes[route_id] = opt_route
        # --- modify routes to minimize distance --- #
        total_distance = 0
        all_route_list = list()
        for key, val in result_routes.items():
            total_distance += self.cal_length(val)
            all_route_list.append(val)
        # first route add the last
        all_route_list.append(all_route_list[0])
        print(all_route_list)
        # return result_routes

        while True:
            ind = 0
            for route1, route2 in zip(all_route_list[:-1], all_route_list[1:]):
                tmp_route1, tmp_route2 = self.modify_route(route1, route2)
                if tmp_route1 != route1 and tmp_route2 != route2:
                    all_route_list[ind] = tmp_route1
                    all_route_list[ind+1] = tmp_route2
                ind += 1

            new_distance = sum([self.cal_length(route) for route in all_route_list[:-1]])
            if new_distance < total_distance:
                for ind, route in enumerate(all_route_list[:-1]):
                    result_routes[ind+1] = route
                total_distance = new_distance
            else:
                return result_routes

    def constraint_capacity(self, current_capa, demand):
        """
        The vehicle capacity constraint
        :param current_capa:
        :param demand:
        :return:
        """
        if current_capa + demand <= self.v_capacity:
            current_capa = current_capa + demand
            return False, current_capa
        else:
            return True, current_capa

    def modify_route(self, route1, route2):
        """
        change the feasible nodes between route1 and route2 to minimize the distance
        :param route1:
        :param route2:
        :return:
        """
        del_node = self.cal_polar_radius(route1)  # the node deleted
        swap_node = self.closest_node(route1[-2], route2)  # the nearest to route1 last node in route2
        # route 1
        tmp_route1 = route1[:-1]
        tmp_route1.remove(del_node.id)
        tmp_route1.insert(0, swap_node.id)
        tmp_route1 = self.tsp_2opt(tmp_route1)
        # route 2
        tmp_route2 = route2[:-1]
        tmp_route2.remove(swap_node.id)
        tmp_route2.insert(0, del_node.id)
        tmp_route2 = self.tsp_2opt(tmp_route2)
        original_distance = self.cal_length(route1) + self.cal_length(route2)
        tmp_distance = self.cal_length(tmp_route1) + self.cal_length(tmp_route2)
        if tmp_distance < original_distance:
            tmp_capa1 = sum([self.customer_list[i-1].demand for i in tmp_route1[1:-1]])
            tmp_capa2 = sum([self.customer_list[i - 1].demand for i in tmp_route2[1:-1]])
            if tmp_capa1 <= self.v_capacity and tmp_capa2 <= self.v_capacity:
                return tmp_route1, tmp_route2
            else:
                return route1, route2
        else:
            return route1, route2


    def cal_polar_radius(self, route):
        """
        find the deleted node
        :param route:
        :param all_nodes:
        :return:
        """
        min_value = float('inf')
        del_node = None
        avr_radius = sum([i.radius for i in self.customer_list])/len(self.customer_list)  # average distance all customers
        for node_index in route[1:-1]:
            node = self.customer_list[node_index-1]
            val = node.radius + node.polar_angle*avr_radius
            if val < min_value:
                min_value = val
                del_node = node
        return del_node

    def closest_node(self, node_id, route):
        """
        find the closest node to route1 last node
        :param node_id:
        :param route:
        :return:
        """
        last_node = self.customer_list[node_id-1]
        min_distance = float('inf')
        swap_node = None
        for node_index in route[1:-1]:
            node = self.customer_list[node_index-1]
            tmp_distance = self.cal_distance(last_node.coordinate, node.coordinate)
            if tmp_distance < min_distance:
                min_distance = tmp_distance
                swap_node = node
        return swap_node

    def tsp_2opt(self, route):
        """
        use 2-opt to get optimal route
        :param route:
        :return:
        """
        num_cities = len(route)
        coordinate = [self.coordinates[i] for i in route]
        tsp_route = tsp2opt.two_opt_algorithm(num_cities, coordinate, self.distance_matrix)
        tmp_route = [route[i] for i in tsp_route]
        depot_index = tmp_route.index(0)
        if depot_index + 1 == len(tmp_route):
            opt_route = [0] + tmp_route
        else:
            opt_route = tmp_route[tmp_route.index(0):] + tmp_route[:tmp_route.index(0) + 1]
        return opt_route


def show_result(city_solution, city_coordinate):
    x_coordinate = []
    y_coordinate = []
    # draw the result
    for city in city_solution:
        x_coordinate.append(city_coordinate[city][0])
        y_coordinate.append(city_coordinate[city][1])
    x_coordinate.append(city_coordinate[city_solution[0]][0]) # end to start
    y_coordinate.append(city_coordinate[city_solution[0]][1])
#         print x_coordinate
    plt.figure(1)
    plt.scatter(x_coordinate,y_coordinate)
    plt.plot(x_coordinate,y_coordinate)
    # draw the city mark
    for city in city_solution:
        plt.text(city_coordinate[city][0], city_coordinate[city][1], city)
    plt.text(city_coordinate[city_solution[0]][0], city_coordinate[city_solution[0]][1], '     Start')   #start
    plt.text(city_coordinate[city_solution[-1]][0], city_coordinate[city_solution[-1]][1], '    End')   #end
    plt.xlabel('City x coordinate')
    plt.ylabel("City y coordinate")
    plt.title("The traveling map by 2_opt")
    plt.grid()
    plt.show()


# ---show the result----#
def print_result(results, distance_matrix):
    route_cnt = 0
    total_distance = 0
    for key, route in results.items():
        total_distance += sum(distance_matrix[i][j] for i, j in zip(route[:-1], route[1:]))
        print('Route %s: %s' % (key, route))
    print('Total distance: %s' % total_distance)


#----------------plot the graph----------#
def show_result(all_routes, coordination):
    for index, route in all_routes.items():
        x = []
        y = []
        # add depot as start and end point
        for j in route:
            x.append(coordination[j][0])
            y.append(coordination[j][1])
            random_color = [i[0] for i in np.random.rand(3, 1)]
            plt.scatter(x, y, c=random_color, marker="*")
            plt.plot(x, y, c=random_color)
    # depot
    z = []
    w = []
    z.append(coordination[0][0])
    w.append(coordination[0][1])
    for index in range(len(coordination)):
        plt.text(coordination[index][0], coordination[index][1], index)
    plt.scatter(z, w, s=100, c="r", marker="o", label="Depot")
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The VRP map by sweep algorithm")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    BASE_DIR = BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'data\A-n32-k5.vrp')
    vehicle_capacity, demand_list, coordinates, distance_matrix = import_data.initData(file_name)
    instance_vrp_sweep = SweepAlgorithm(vehicle_capacity, demand_list, coordinates, distance_matrix)
    opt_result = instance_vrp_sweep.run()
    print_result(opt_result, distance_matrix)
    show_result(opt_result, coordinates)

    # instance
    # A-n32-k5.vrp
    # A-n33-k5.vrp
    # A-n33-k6.vrp
    # A-n45-k7.vrp
    # A-n65-k9.vrp
    # A-n80-k10.vrp
