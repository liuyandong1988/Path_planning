#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/16 6:51
# Description: ‘A Heuristic Algorithm for the Vehicle-Dispatch Problem’ by Billy E.
#               Operations Research, Vol. 22, No. 2 (Mar. - Apr., 1974), pp. 340-349Published
#               (1) sweep algorithm
#               (2) 2-opt tsp

import import_Auger, import_Chris
import os, math, time
import two_optimal
from matplotlib import pyplot as plt


class Node(object):

    def __init__(self, id, coordinate, demand = 0):
        self.id = id
        self.coordinate = coordinate
        self.demand = demand
        self.polar_angle = 0
        self.radius = 0


class SweepAlgorithm(object):

    def __init__(self, vehicle_capacity, vehicle_endurance, service_time, demand_list, coordinates, distance_matrix):
        self.v_capacity = vehicle_capacity
        self.v_endurance = vehicle_endurance
        self.node_service_time = service_time
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
        """
        calculate the polar of node and sorting
        :return:
        """
        d_coordinate = self.coordinates[0]
        c_coordinates = self.coordinates[1:]
        node_id = 1
        self.store_info = list()
        # print(len(c_coordinates))
        for ind, c_coordinate in enumerate(c_coordinates):
            if c_coordinate[0]-d_coordinate[0] == 0:
                if c_coordinate[1]-d_coordinate[1] > 0:
                    angle_tmp = math.pi / 2
                else:
                    angle_tmp = - math.pi / 2

            else:
                angle_tmp = math.atan((c_coordinate[1]-d_coordinate[1])/(c_coordinate[0]-d_coordinate[0]))
            if c_coordinate[1]-d_coordinate[1] < 0:
                if angle_tmp > 0:
                    angle_tmp = -math.pi + angle_tmp
                else:
                    pass
            elif c_coordinate[1] == d_coordinate[1]:
                if c_coordinate[0] > d_coordinate[0]:
                    pass
                else:
                    angle_tmp = - math.pi
            else:
                if angle_tmp > 0:
                    pass
                else:
                    angle_tmp = math.pi + angle_tmp

            radius_tmp = (math.sqrt(math.pow(c_coordinate[0]-d_coordinate[0], 2)
                                    + math.pow(c_coordinate[1]-d_coordinate[1], 2)))
            self.store_info.append([node_id, angle_tmp, radius_tmp])
            self.customer_list[ind].polar_angle = angle_tmp
            self.customer_list[ind].radius = radius_tmp
            node_id += 1
        # sorting increase
        self.store_info.sort(key=lambda x: x[1], reverse=False)
        print('Sorting:', self.store_info)
        # for index, node in enumerate(coordinates):
        #     plt.scatter(node[0], node[1], c='r')
        #     plt.text(node[0], node[1], index)
        # plt.show()

    def cal_route_distance(self, route):
        """
        calculate the route length
        :param route:
        :return:
        """
        return sum(self.distance_matrix[i][j] for i, j in zip(route[:-1], route[1:]))

    def cal_solution_distance(self, solution):
        """
        calculate the solution total distance
        """
        total_distance = 0
        for key, route in solution.items():
            total_distance += self.cal_route_distance(route)
        return total_distance

    def generate_new_route(self, r_id, r_opt, remain_n, r_new):
        r_id += 1
        for node in r_opt[1:-1]:
            remain_n.remove(node)
        capacity = 0
        n_pos = 0
        r_new.clear()
        # show_result({1: opt_route}, self.coordinates)
        # print('nodes:', remain_nodes)
        return r_id, remain_n, r_new, n_pos, capacity

    def check_capacity(self, current_capacity, demand):
        """
        The vehicle capacity constraint
        :return:
        """
        if current_capacity + demand <= self.v_capacity:
            current_capacity += demand
            return False, current_capacity
        else:
            return True, current_capacity

    def check_route_capacity(self, route):
        """
        A route demand satisfy the capacity constraint
        """
        if sum([self.c_demand[node] for node in route]) <= self.v_capacity:
            return True
        else:
            return False

    def check_distance(self, route, distance):
        """
        check the distance constraint
        """
        node_num = len(route)-2
        while (distance + node_num*self.node_service_time) > self.v_endurance:
            route.pop(-2)
            node_num -= 1
            distance = self.cal_route_distance(route)
        return route, distance

    def opt_new_route(self, route):
        """
        optimize the route by 2-opt
        :param route:
        :return:
        """
        route.insert(0, 0)
        route.append(0)  # add the depot
        opt_route = two_optimal.two_opt(route, self.distance_matrix)
        distance = self.cal_route_distance(opt_route)
        return opt_route, distance

    def find_key_node(self, route, remain_n):
        """
        find the three node:
        nearest node to the last node in route,
        second nearest node,
        delete node in route
        :param route:
        :return:
        """
        last_node = route[-2]
        find_node_set = remain_n[:]
        for node in route[1:-1]:
            find_node_set.remove(node)
        distance_list = distance_matrix[last_node].tolist()
        distance_list[0] = float('inf')
        distance_list_min = [distance_list[i] for i in find_node_set]
        distance_list_min.sort()
        node1 = distance_list.index(distance_list_min[0])
        distance_list[node1] = float('inf')
        try:
            second = distance_list_min[1]
        except IndexError:
            node2 = None
        else:
            node2 = distance_list.index(second)
        del_node = self.cal_polar_radius(route)
        return node1, node2, del_node

    def cal_polar_radius(self, each_route):
        """
        find the deleted node: the nearest depot
        :param each_route:
        :param all_nodes:
        :return:
        """
        min_value = float('inf')
        del_node = None
        avr_radius = sum([i.radius for i in self.customer_list]) / len(self.customer_list)  # average distance all customers
        for node_index in each_route[1:-1]:
            node = self.customer_list[node_index - 1]
            val = node.radius + node.polar_angle * avr_radius
            if val < min_value:
                min_value = val
                del_node = node
        return del_node.id

    def run(self):
        """
        cluster based on the polar
        :return:
        """
        all_solution = dict()
        all_nodes = len(self.store_info)
        for rotate_i in range(all_nodes):
            # rotate all nodes construct the new combination
            route_id = 1
            all_route = dict()
            remain_nodes = [n[0] for n in self.store_info]  # remain to optimize node
            remain_nodes = remain_nodes[rotate_i:] + remain_nodes[:rotate_i]
            # --- vrp by sweep algorithm --- #
            node_pos = 0  # the node position in the remain_nodes
            tmp_capacity = 0
            new_route = list()
            # print('nodes:', remain_nodes)
            while remain_nodes:
                try:
                    next_node = remain_nodes[node_pos]
                except IndexError:
                    # the remain nodes form a route
                    opt_route, route_distance = self.opt_new_route(new_route)
                    opt_route, route_distance = self.check_distance(opt_route, route_distance)
                    all_route[route_id] = opt_route
                    all_route_distance = self.cal_solution_distance(all_route)
                    all_solution[all_route_distance] = all_route
                    print('Total %d nodes, iteration: %d, distance: %.03f' % (all_nodes, rotate_i, all_route_distance))
                    # print(all_route)
                    # show_result(all_route, self.coordinates)
                    break
                else:
                    overload_mark, tmp_capacity = self.check_capacity(tmp_capacity, self.c_demand[next_node])
                if overload_mark:
                    # --- generate a route and optimize by 2-opt --- #
                    opt_route = new_route[:]
                    opt_route, route_distance = self.opt_new_route(opt_route)
                    # --- check the distance constraint --- #
                    opt_route, route_distance = self.check_distance(opt_route, route_distance)
                    # print('1#', opt_route, route_distance)
                    # show_result({1:opt_route}, self.coordinates)
                    # --- find the three node:
                    # nearest node to the last node in route, second nearest node, delete node in route --- #
                    node1, node2, del_node = self.find_key_node(opt_route, remain_nodes)
                    # print('*', node1, node2, del_node)
                    # --- calculate the route add node1 and del del_node (tsp distance) --- #
                    route_2 = opt_route[1:-1]
                    route_2.remove(del_node)
                    route_2.append(node1)
                    route_2, route_distance_2 = self.opt_new_route(route_2)
                    # print('2#', route_2, route_distance_2)
                    # - 2 condition: distance and capacity
                    if route_distance_2 <= route_distance and self.check_route_capacity(route_2):
                        route_3_first_node = remain_nodes[node_pos]
                        route_3 = [route_3_first_node]
                        for i in range(5):
                            try:
                                n = remain_nodes[node_pos+i+1]
                            except IndexError:
                                # print('No remain nodes !')
                                continue
                            else:
                                route_3.append(n)
                        route_3, route_distance_3 = self.opt_new_route(route_3)
                        # minus the last node to depot distance
                        route_distance_3 -= self.distance_matrix[0][route_3[-2]]
                        if node1 in route_3:
                            route_4 = route_3[1:-1]
                            route_4.remove(node1)
                            route_4.append(del_node)
                            route_4, route_distance_4 = self.opt_new_route(route_4)
                        else:
                            # - restore the optimal route
                            all_route[route_id] = opt_route
                            # - modify the parameter and generate a new route
                            route_id, remain_nodes, new_route, node_pos, tmp_capacity = \
                                self.generate_new_route(route_id, opt_route, remain_nodes, new_route)
                            continue
                        if route_distance + route_distance_3 < route_distance_2 + route_distance_4:
                            # modify two nodes
                            if node1 in route_3 and node2 in route_3:
                                route_5 = opt_route[1:-1]
                                route_5.remove(del_node)
                                route_5.append(node1)
                                route_5.append(node2)
                                route_5, route_distance_5 = self.opt_new_route(route_5)
                                if route_distance_5 < route_distance and self.check_route_capacity(route_5):
                                    route_6_first_node = remain_nodes[node_pos]
                                    route_6 = [route_6_first_node]
                                    for i in range(5):
                                        try:
                                            n = remain_nodes[node_pos + i + 1]
                                        except IndexError:
                                            # print('No remain nodes !')
                                            continue
                                        else:
                                            route_6.append(n)
                                    route_6, route_distance_6 = self.opt_new_route(route_6)
                                    # minus the last node to depot distance
                                    route_distance_6 -= self.distance_matrix[0][route_6[-2]]
                                    if route_distance + route_distance_3 < route_distance_5 + route_distance_6:
                                        # - restore the optimal route
                                        all_route[route_id] = opt_route
                                        # - modify the parameter and generate a new route
                                        route_id, remain_nodes, new_route, node_pos, tmp_capacity = \
                                            self.generate_new_route(route_id, opt_route, remain_nodes, new_route,
                                                                    node_pos)
                                        continue
                                    else:
                                        # modify route
                                        opt_route.remove(del_node)
                                        opt_route.insert(-1, node1)
                                        opt_route.insert(-1, node2)
                                        opt_route, route_distance = self.opt_new_route(opt_route[1:-1])
                                        opt_route, route_distance = self.check_distance(opt_route, route_distance)
                                        # - restore the optimal route
                                        all_route[route_id] = opt_route
                                        # - modify the parameter and generate a new route
                                        route_id, remain_nodes, new_route, node_pos, tmp_capacity = \
                                            self.generate_new_route(route_id, opt_route, remain_nodes, new_route)
                                        continue

                                else:
                                    # - restore the optimal route
                                    all_route[route_id] = opt_route
                                    # - modify the parameter and generate a new route
                                    route_id, remain_nodes, new_route, node_pos, tmp_capacity = \
                                        self.generate_new_route(route_id, opt_route, remain_nodes, new_route)
                                    continue
                            else:
                                # - restore the optimal route
                                all_route[route_id] = opt_route
                                # - modify the parameter and generate a new route
                                route_id, remain_nodes, new_route, node_pos, tmp_capacity = \
                                    self.generate_new_route(route_id, opt_route, remain_nodes, new_route)
                                continue
                        else:
                            # modify route
                            opt_route.remove(del_node)
                            opt_route.insert(-1, node1)
                            opt_route, route_distance = self.opt_new_route(opt_route[1:-1])
                            opt_route, route_distance = self.check_distance(opt_route, route_distance)
                            # - restore the optimal route
                            all_route[route_id] = opt_route
                            # - modify the parameter and generate a new route
                            route_id, remain_nodes, new_route, node_pos, tmp_capacity = \
                                self.generate_new_route(route_id, opt_route, remain_nodes, new_route)
                            continue
                    else:
                        # - restore the optimal route
                        all_route[route_id] = opt_route
                        # - modify the parameter and generate a new route
                        route_id, remain_nodes, new_route, node_pos, tmp_capacity = \
                            self.generate_new_route(route_id, opt_route, remain_nodes, new_route)
                else:
                    # satisfy the capacity constraint
                    new_route.append(next_node)
                    node_pos += 1
        return all_solution


# ---show the result----#
def print_result(results, distance_matrix):
    route_cnt = 0
    total_distance = 0
    for key, route in results.items():
        total_distance += sum(distance_matrix[i][j] for i, j in zip(route[:-1], route[1:]))
        print('Route %s: %s' % (key, route))
    print('Total distance: %s' % total_distance)


# ---plot the graph --- #
def show_result(all_routes, coordination):
    for index, route in all_routes.items():
        x = []
        y = []
        # add depot as start and end point
        for j in route:
            x.append(coordination[j][0])
            y.append(coordination[j][1])
            # random_color = [i[0] for i in np.random.rand(3, 1)]
            plt.scatter(x, y, c='r', marker="*")
            plt.plot(x, y, c='g')
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
    file_name = os.path.join(BASE_DIR, 'data\Christofides1979\CMT3.vrp')
    # --- for different data
    pos = file_name.find('data')
    data_name = file_name[pos+5:pos+10]
    if data_name == 'Chris':
        vehicle_capacity, vehicle_endurance, service_time, demand_list, coordinates, distance_matrix = import_Chris.init_data(file_name)
    elif data_name == 'Auger':
        vehicle_capacity, demand_list, coordinates, distance_matrix = import_Auger.init_data(file_name)
        vehicle_endurance = float('inf')
    # --- optimize by sweep algorithm
    start_time = time.time()
    instance_vrp_sweep = SweepAlgorithm(vehicle_capacity, vehicle_endurance,service_time, demand_list, coordinates, distance_matrix)
    all_solution = instance_vrp_sweep.run()
    print('Running time %.03f' % (time.time() - start_time))
    # --- print the best solution
    min_distance = min(all_solution.keys())
    best_solution = all_solution[min_distance]
    for key, route in best_solution.items():
        distance_route = sum(distance_matrix[i][j] for i, j in zip(route[:-1], route[1:])) + (len(route)-2)*service_time
        demand_route = sum(demand_list[i] for i in route)
        print('Route %s - %.03f - %d :%s' % (key, distance_route, demand_route, route))
    print('Total distance: %s' % min_distance)
    show_result(best_solution, coordinates)

    # instance
    # 'data\Augerat1995\A-n32-k5.vrp'
    # A-n32-k5.vrp
    # A-n33-k5.vrp
    # A-n33-k6.vrp
    # A-n45-k7.vrp
    # A-n65-k9.vrp
    # A-n80-k10.vrp
    # 'data\Christofides1979\CMT1.vrp'
