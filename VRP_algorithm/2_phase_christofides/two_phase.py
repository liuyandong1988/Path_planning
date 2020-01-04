#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/18 0:33
# create the initial solution randomly and optimize by 2-opt and 3-opt
# choose the best solution
import import_data
import math, random
from r_optimal import two_optimal, three_optimal
import support as sp


def configure_vehicle(route, demand_list, vehicle_capacity):
    """
    configure the vehicle by demand
    :param route:
    :param demand_list:
    :param vehicle_capacity:
    :return:
    """
    tmp_capacity = 0
    tmp_route = list()
    route_num = 1
    configure_solution = dict()
    for node in route:
        if tmp_capacity + demand_list[node] <= vehicle_capacity:
            # allow add the demand
            tmp_capacity += demand_list[node]
            tmp_route.append(node)
        else:
            # complete route and create a new route
            # print(tmp_route)
            tmp_route = [0] + tmp_route[:] + [0]
            # --- optimize by 2-opt --- #
            two_opt_route = two_optimal.two_opt(tmp_route, distance_matrix)
            configure_solution[route_num] = two_opt_route  # add the start and end
            tmp_capacity = demand_list[node]
            tmp_route = [node]
            route_num += 1
    # the last route
    configure_solution[route_num] = [0] + tmp_route[:] + [0]
    # print(configure_solution)
    # input('123')
    return configure_solution


def two_phase(vehicle_capacity, demand_list, distance_matrix, coordinates, times = 3):
    """
    The initial random feasible route and optimize each route by r-opt
    configure vehicle by demand list
    :param vehicle_capacity:
    :param demand_list:
    :param distance_matrix:
    :param times: iteration and different the initial solution
    :return: the best solution
    """
    # --- a random feasible route --- #
    min_cost = float('inf')
    node_number = len(coordinates)
    for iteration in range(times):
        initial_route = list(range(1, node_number))
        random.shuffle(initial_route)
        random_route = [0] + initial_route +[0]
        # --- optimize by 2-opt --- #
        two_opt_route = two_optimal.two_opt(random_route, distance_matrix)
        # print('2-opt: %s' % two_opt_route)
        # --- optimize by 3-opt --- #
        three_opt_route = two_opt_route[:-1]  # except the end depot
        three_opt_route = three_optimal.three_optimal(three_opt_route, distance_matrix)
        # print('3-opt: %s' % three_opt_route)
        # sp.show_route(three_opt_route, coordinates)
        # --- configure the vehicle by demand --- #
        configure_route = three_opt_route[1:]  # except the start depot
        tmp_solution = configure_vehicle(configure_route, demand_list, vehicle_capacity)
        tmp_cost = 0
        # --- the cost of solution --- #
        for key, route in tmp_solution.items():
            tmp_cost += sp.calculate_cost(route, distance_matrix)
        if tmp_cost < min_cost:
            final_solution = tmp_solution
            min_cost = tmp_cost
        print('Iteration %s Min cost: %.3f Route: %s' % (iteration, min_cost, final_solution))
    return final_solution, min_cost


if __name__ == '__main__':
    import os
    BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'data\A-n32-k5.vrp')
    vehicle_capacity, demand_list, coordinates, distance_matrix = import_data.init_data(file_name)
    best_solution, min_cost = two_phase(vehicle_capacity, demand_list, distance_matrix, coordinates)
    print('The min cost %s routes: %s'%(min_cost, best_solution))
    sp.show_result(best_solution, coordinates)

    # instance
    # A-n32-k5.vrp
    # A-n45-k6.vrp
    # A-n55-k9.vrp
    # A-n69-k9.vrp
    # A-n80-k10.vrp

