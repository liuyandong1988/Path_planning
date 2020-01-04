#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/16 6:51
# Description: ‘Scheduling of Vehicles from a Central Depot to a Number of Delivery Points’ by G. Clarke
#               Operations Research, Vol. 12, No. 4. (Jul. - Aug., 1964), pp. 568-581
#               (1) running fast
#               (2) near-optimum
#               (3) not least vehicles

import os, time
import import_data
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.abspath('.')
all_routes = dict()
route_id = None


class Route(object):
    """
     The class of route, and the method to create, merge, add ...
    """

    def __init__(self, id, nodes, demand, vehicle_capacity):
        self.id = id
        self.nodes = nodes
        self.start_end()
        self.demand = demand
        self.merge_mark = False
        self.merge_not_mark = False
        self.vehicle_capacity = vehicle_capacity
        self.add_new(nodes, demand)

    def start_end(self):
        if len(self.nodes) == 1:
            self.start = self.nodes[0]
            self.end = self.nodes[0]
        else:
            self.start = self.nodes[0]
            self.end = self.nodes[1]

    def add_new(self, nodes, demand):
        self.path = list(nodes)
        self.capacity = sum([demand[i] for i in nodes])

    def check_in(self, cand_nodes):
        """
        check the node is start/end, merge node or not
        """
        global all_routes, route_id
        node_1, node_2 = cand_nodes[0], cand_nodes[1]
        if node_1 in [self.start, self.end] and node_2 in [self.start, self.end]:
            # both nodes are start or end
            return False
        elif node_1 in [self.start, self.end] or node_2 in [self.start, self.end]:
            # one of nodes is start or end
            if node_1 == self.start:
                for key, val in all_routes.items():
                    other = val.path
                    if node_2 == other[0]:
                        self.merge_route(other[::-1], self.path)
                    elif node_2 == other[-1]:
                        self.merge_route(other, self.path)
                    if self.merge_mark:
                        # satisfy the capacity and then merge the routes
                        del all_routes[key]
                        return True
            elif node_1 == self.end:
                for key, val in all_routes.items():
                    other = val.path
                    if node_2 == other[0]:
                        self.merge_route(self.path, other)
                    elif node_2 == other[-1]:
                        self.merge_route(self.path, other[::-1])
                    if self.merge_mark:
                        # satisfy the capacity and then merge the routes
                        del all_routes[key]
                        return True
            elif node_2 == self.start:
                for key, val in all_routes.items():
                    other = val.path
                    if node_1 == other[0]:
                        self.merge_route(other[::-1], self.path)
                    elif node_1 == other[-1]:
                        self.merge_route(other, self.path)
                    if self.merge_mark:
                        # satisfy the capacity and then merge the routes
                        del all_routes[key]
                        return True
            elif node_2 == self.end:
                for key, val in all_routes.items():
                    other = val.path
                    if node_1 == other[0]:
                        self.merge_route(self.path, other)
                    elif node_1 == other[-1]:
                        self.merge_route(self.path, other[::-1])
                    if self.merge_mark:
                        # satisfy the capacity and then merge the routes
                        del all_routes[key]
                        return True
            return True
        else:
            return False

    def merge_route(self, one_route, other):
        """
        merge the path with another route
        merge path capacity
        """
        capacity = sum([self.demand[i] for i in one_route + other])
        if capacity <= self.vehicle_capacity:
            self.merge_mark = True
            self.path = one_route + other
            self.start = self.path[0]
            self.end = self.path[-1]
            self.capacity = capacity
        else:
            self.merge_not_mark = True
            pass

    def add_candidate(self, cand_nodes):
        """
        Add to the current route
        """
        for node_i in cand_nodes:
            if node_i == self.start:
                two_nodes = list(cand_nodes)
                two_nodes.remove(node_i)
                other_node = two_nodes[0]
                if self.check_capacity(other_node):
                    self.path.insert(0, other_node)
                    self.start = other_node
                    self.capacity += self.demand[other_node]
                return
            elif node_i == self.end:
                two_nodes = list(cand_nodes)
                two_nodes.remove(node_i)
                other_node = two_nodes[0]
                if self.check_capacity(other_node):
                    self.path.append(other_node)
                    self.end = other_node
                    self.capacity += self.demand[other_node]
                return

    def check_capacity(self, add_node):
        if self.capacity + self.demand[add_node] <= self.vehicle_capacity:
            return True
        else:
            return False


def saving_sort(demand_list, vehicle_capacity, distance_matrix):
    """
    Get the saving list in increased order.
    d[0][i] + d[0][j] - d[i][j]
    return saving list [(i, j), saving_distance]
    """
    node_num = len(distance_matrix)
    saving_matrix = np.zeros([node_num, node_num])
    for i in range(node_num):
        for j in range(node_num):
            if i == j:
                saving_matrix[i][j] = 0
            else:
                if demand_list[i] + demand_list[j] > vehicle_capacity:
                    saving_matrix[i][j] = 0
                else:
                    saving_matrix[i][j] = distance_matrix[0][i] + distance_matrix[0][j] - distance_matrix[i][j]

    saving_list = list()
    for i in range(1, node_num - 1):
        for j in range(i + 1, node_num):
            if saving_matrix[i][j] == 0:
                pass
            else:
                saving_list.append([(i, j), saving_matrix[i][j]])
    # sorting decrease
    saving_list.sort(key=lambda x: x[1], reverse=False)
    return saving_list


def check_alone_node(remain_nodes):
    """
    Node demand is over the capacity constraint and forms route by itself
    """
    global all_routes, route_id
    for node in remain_nodes:
        route_id += 1
        new_route = Route(route_id, node, demand_list, vehicle_capacity)
        all_routes[route_id] = new_route


def saving_algorithm(distance_matrix, demand_list, vehicle_capacity):
    """
    Clarke and Wright: saving algorithm
    """
    # calculate the saving list

    global all_routes, route_id

    saving_list = saving_sort(demand_list, vehicle_capacity, distance_matrix)

    visited = list()
    interior_nodes = list()
    route_id = 0
    all_routes[route_id] = list()
    current_route = all_routes[route_id]
    start_time = time.time()
    # merge the parts in the saving list
    while saving_list:
        candidate_part = saving_list.pop()
        cand_nodes, _ = candidate_part[0], candidate_part[1]
        # --- the first route --- #
        if not current_route:
            # current route is empty
            current_route = Route(route_id, cand_nodes, demand_list, vehicle_capacity)
            all_routes[route_id] = current_route
            visited.extend(current_route.path)
            continue
        # --- if one of the nodes is the interior node and pass --- #
        if cand_nodes[0] in interior_nodes or cand_nodes[1] in interior_nodes:
            continue
        # --- two nodes are not in the exist routes --- #
        if cand_nodes[0] not in visited and cand_nodes[1] not in visited:
            # create a new route
            route_id += 1
            new_route = Route(route_id, cand_nodes, demand_list, vehicle_capacity)
            all_routes[route_id] = new_route
            visited.extend(new_route.path)
            continue
        else:
            for r_id, current_route in all_routes.items():
                if current_route.check_in(cand_nodes):
                    if current_route.merge_mark or current_route.merge_not_mark:
                        # -- merge -- #
                        current_route.merge_mark = False
                        current_route.merge_not_mark = False
                    else:
                        # -- add -- #
                        current_route.add_candidate(cand_nodes)
                    interior_nodes.extend(current_route.path[1:-1])  # visited the interior nodes
                    visited.extend(current_route.path)
                    break
                else:
                    pass
                    # --- not satisfy the capacity or other reason --- #
    # --- check the remain nodes --- #
    all_nodes = list(range(len(demand_list)))
    all_nodes.remove(0)
    remain_nodes = [all_nodes.remove(i) for i in list(set(visited))]
    if remain_nodes == []:
        check_alone_node(remain_nodes)
    else:
        pass

    result_routes = list()
    for key, route in all_routes.items():
        result_routes.append(route.path)
    print('The running time %s'%(time.time() - start_time))
    return result_routes


# ---show the result----#
def print_result(results, distance_matrix):
    route_cnt = 0
    total_distance = 0
    for route in results:
        route_cnt += 1
        depot_route = [0] + route + [0]
        total_distance += sum(distance_matrix[i][j] for i, j in zip(depot_route[:-1], depot_route[1:]))
        print('Route %s: %s' % (route_cnt, depot_route))
    print('Total distance: %s' % total_distance)


# ---  plot the graph  --- #
def show_result(all_routes, coordination):
    for index, route in enumerate(all_routes):
        x = []
        y = []
        # add depot as start and end point
        for j in [0] + route + [0]:
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
    plt.title("The VRP map by saving algorithm")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    file_name = os.path.join(BASE_DIR, 'data\A-n32-k5.vrp')
    vehicle_capacity, demand_list, coordination, distance_matrix = import_data.initData(file_name)
    results = saving_algorithm(distance_matrix, demand_list, vehicle_capacity)
    print_result(results, distance_matrix)
    show_result(results, coordination)
# instance
# A-n32-k5.vrp
# A-n45-k6.vrp
# A-n55-k9.vrp
# A-n69-k9.vrp
# A-n80-k10.vrp