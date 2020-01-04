# !/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
import import_Chris
import time, math
import two_optimal


def polar_sort(coordinates):
    """
    calculate the polar of node and sorting
    :return:
    """
    d_coordinate = coordinates[0]
    c_coordinates = coordinates[1:]
    node_id = 1
    store_info = list()
    for ind, c_coordinate in enumerate(c_coordinates):
        if c_coordinate[0] - d_coordinate[0] == 0:
            if c_coordinate[1] - d_coordinate[1] > 0:
                angle_tmp = math.pi / 2
            else:
                angle_tmp = - math.pi / 2

        else:
            angle_tmp = math.atan((c_coordinate[1] - d_coordinate[1]) / (c_coordinate[0] - d_coordinate[0]))
        if c_coordinate[1] - d_coordinate[1] < 0:
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

        radius_tmp = (math.sqrt(math.pow(c_coordinate[0] - d_coordinate[0], 2)
                                + math.pow(c_coordinate[1] - d_coordinate[1], 2)))
        store_info.append([node_id, angle_tmp, radius_tmp])
        # customer_list[ind].polar_angle = angle_tmp
        # customer_list[ind].radius = radius_tmp
        node_id += 1
    # sorting increase
    store_info.sort(key=lambda x: x[1], reverse=False)
    return store_info

def check_capacity(current_capacity, demand):
    """
    The vehicle capacity constraint
    :return:
    """
    if current_capacity + demand <= vehicle_capacity:
        current_capacity += demand
        return False, current_capacity
    else:
        return True, current_capacity


def check_distance(route, distance):
    """
    check the distance constraint
    """
    node_num = len(route)-2
    while (distance + node_num*service_time) > vehicle_endurance:
        route.pop(-2)
        node_num -= 1
        distance = cal_route_distance(route)
    return route, distance

def cal_route_distance(route):
    """
    calculate the route length

    """
    return sum(distance_matrix[i][j] for i, j in zip(route[:-1], route[1:]))


def opt_new_route(route):
    """
    optimize the route by 2-opt
    :param route:
    :return:
    """
    route.insert(0, 0)
    route.append(0)  # add the depot
    opt_route = two_optimal.two_opt(route, distance_matrix)
    distance = cal_route_distance(opt_route)
    return opt_route, distance


def initial_routes(customers, depot):
    """
    assign customers to vehicles starting by the sweep
    """
    # --- initial routes by polar angle --- #
    store_info = polar_sort(coordinates)
    # --- create the new route --- #
    tmp_capacity = 0
    route_node = list()
    all_route = dict()
    all_route_distance = dict()
    route_id = 1
    remain_nodes = [n[0] for n in store_info]
    node_pos = 0  # the node position in the remain_nodes
    while remain_nodes:
        try:
            next_node = remain_nodes[node_pos]
        except IndexError:
            opt_route = route_node[:]
            opt_route, route_distance = opt_new_route(opt_route)
            route, distance = check_distance(opt_route, route_distance)
            # generate a route
            all_route[route_id] = route
            all_route_distance[route_id] = distance
            # aa = all_route.values()
            # show_result(aa, coordinates)
            break
        else:
            # --- check capacity constrain --- #
            overload_mark, tmp_capacity = check_capacity(tmp_capacity, demand_list[next_node])
            if overload_mark:
                # --- check the distance constraint --- #
                opt_route = route_node[:]
                opt_route, route_distance = opt_new_route(opt_route)
                route, distance = check_distance(opt_route, route_distance)
                # generate a route
                all_route[route_id] = route
                all_route_distance[route_id] = distance
                # reset new route
                for node in route[1:-1]:
                    remain_nodes.remove(node)
                route_id += 1
                route_node.clear()
                tmp_capacity = 0
                node_pos = 0
            else:
                route_node.append(next_node)
                node_pos += 1

    return all_route, all_route_distance


def cal_each_route_cost(vehicle_tour, depot, distance_matrix):
    obj = 0
    if len(vehicle_tour) > 0:
        obj += distance_matrix[depot.index][vehicle_tour[0].index]
        for i in range(0, len(vehicle_tour) - 1):
            obj += distance_matrix[vehicle_tour[i].index][vehicle_tour[i + 1].index]
        obj += distance_matrix[vehicle_tour[-1].index][depot.index]
    return obj


def cal_route_cost(route_count, vehicle_tours, depot, distance_matrix):
    """
    calculate the real total distance
    """
    obj = 0
    for v in range(0, route_count):
        vehicle_tour = vehicle_tours[v]
        obj += cal_each_route_cost(vehicle_tour, depot, distance_matrix)
    print('The cost of route is %s' % obj)
    return obj


def cal_each_augmented_cost(vehicle_tour, depot, distance_matrix, param_lambda, penalty):
    """
    The distance by each route.
    """
    augmented_obj = 0
    if len(vehicle_tour) > 0:
        augmented_obj += distance_matrix[depot.index][vehicle_tour[0].index] + \
                         param_lambda * penalty[depot.index][vehicle_tour[0].index]
        for i in range(0, len(vehicle_tour) - 1):
            augmented_obj += distance_matrix[vehicle_tour[i].index][vehicle_tour[i + 1].index] + \
                             param_lambda * penalty[vehicle_tour[i].index][vehicle_tour[i + 1].index]
        augmented_obj += distance_matrix[vehicle_tour[-1].index][depot.index] + \
                         param_lambda * penalty[vehicle_tour[-1].index][depot.index]
    return augmented_obj


def cal_route_augmented_cost(route_count, vehicle_tours, depot, distance_matrix, param_lambda, penalty):
    """
    Calculate the total distance with augmented.
    """
    augmented_obj = 0
    for v in range(0, route_count):
        vehicle_tour = vehicle_tours[v]
        augmented_obj += cal_each_augmented_cost(vehicle_tour, depot, distance_matrix, param_lambda, penalty)

    print('The augmented cost of route is %s' % augmented_obj)
    return augmented_obj


def neighbor_relocate(vehicle_tours, customers, vehicle_capacity, distance_matrix, penalty, param_lambda):
    """
    locate search by relocate
    """
    # check_route = list()
    # for index_a, tour_a in enumerate(vehicle_tours):
    #     for node in tour_a:
    #         check_route.append(node[0])
    #     print(check_route)
    #     check_route = list()
    # print('----'*10)


    depot = customers[0]
    max_augmented_cost_gain = -float('inf')
    for index_a, tour_a in enumerate(vehicle_tours):
        for index_b, tour_b in enumerate(vehicle_tours):
            if tour_a == tour_b:
                continue
            for node_a in tour_a:
                # customer_index = node_a.index
                tour_b_capacity = sum([i.demand for i in tour_b])
                if node_a.demand > vehicle_capacity - tour_b_capacity:
                    continue
                tour_b.append(depot)  # add insert position
                for pos, node_b in enumerate(tour_b):
                    new_tour_a = tour_a[:]
                    new_tour_b = tour_b[:]
                    # print("1", new_tour_a)
                    # print("1", new_tour_b)
                    # insert the customer
                    new_tour_b.insert(pos, node_a)
                    # check the distance satisfaction
                    if vehicle_endurance != float('inf'):
                        check_route = list()
                        for node in new_tour_b:
                            check_route.append(node[0])
                        rt, dt = opt_new_route(check_route[:-1])
                        if dt+(len(rt)-2)*service_time > vehicle_endurance:
                            continue
                    # delete the customer
                    new_tour_a.remove(node_a)
                    # print("2", new_tour_a)
                    # print("2", new_tour_b)
                    new_tour_b.pop()
                    augmented_cost_old = (cal_each_augmented_cost(tour_a, depot, distance_matrix, param_lambda, penalty)
                                          + cal_each_augmented_cost(tour_b, depot, distance_matrix, param_lambda,
                                                                    penalty))
                    augmented_cost_new = (
                                cal_each_augmented_cost(new_tour_a, depot, distance_matrix, param_lambda, penalty)
                                + cal_each_augmented_cost(new_tour_b, depot, distance_matrix, param_lambda, penalty))
                    augmented_cost_gain = augmented_cost_old - augmented_cost_new  # the more the better
                    if max_augmented_cost_gain >= augmented_cost_gain:
                        continue
                    cost_old = (cal_each_route_cost(tour_a, depot, distance_matrix) +
                                cal_each_route_cost(tour_b, depot, distance_matrix))
                    cost_new = (cal_each_route_cost(new_tour_a, depot, distance_matrix) +
                                cal_each_route_cost(new_tour_b, depot, distance_matrix))
                    cost_gain = cost_old - cost_new
                    # update
                    max_augmented_cost_gain = augmented_cost_gain
                    max_cost_gain = cost_gain
                    max_new_tour_a = [index_a, new_tour_a[:]]
                    max_new_tour_b = [index_b, new_tour_b[:]]
                    relocate_feasible = True
                tour_b.pop()
    if max_augmented_cost_gain < 1e-6:
        max_augmented_cost_gain = -float('inf')
        max_cost_gain = -float('inf')
        max_new_tour_a = None
        max_new_tour_b = None
        relocate_feasible = False

    return max_augmented_cost_gain, max_cost_gain, max_new_tour_a, max_new_tour_b, relocate_feasible


def neighbor_exchange(vehicle_tours, customers, vehicle_capacity, distance_matrix, penalty, param_lambda):
    """
    locate search by exchange
    """
    max_augmented_cost_gain = -float('inf')
    for index_a, tour_a in enumerate(vehicle_tours):
        for index_b, tour_b in enumerate(vehicle_tours):
            if tour_a == tour_b:
                continue
            for pos_a, node_a in enumerate(tour_a):
                for pos_b, node_b in enumerate(tour_b):
                    tour_a_remain_capacity = vehicle_capacity - sum([i.demand for i in tour_a])
                    tour_b_remain_capacity = vehicle_capacity - sum([i.demand for i in tour_b])
                    if tour_a_remain_capacity + node_a.demand < node_b.demand:
                        continue
                    if tour_b_remain_capacity + node_b.demand < node_a.demand:
                        continue
                    new_tour_a = tour_a[:]
                    new_tour_b = tour_b[:]
                    # swap the node in two different routes
                    new_tour_a[pos_a], new_tour_b[pos_b] = node_b, node_a
                    involve_constraint = False
                    if vehicle_endurance != float('inf'):
                        # check two new route distance constraint:
                        for new_tour in [new_tour_a, new_tour_b]:
                            check_route = list()
                            for node in new_tour:
                                check_route.append(node[0])
                            rt, dt = opt_new_route(check_route)
                            if dt+(len(rt)-2)*service_time > vehicle_endurance:
                                involve_constraint = True
                                break
                        if involve_constraint:
                            continue
                    # calculate the cost old routes and exchanged routes
                    depot = customers[0]
                    augmented_cost_old = (cal_each_augmented_cost(tour_a, depot, distance_matrix, param_lambda, penalty)
                                          + cal_each_augmented_cost(tour_b, depot, distance_matrix, param_lambda,
                                                                    penalty))
                    augmented_cost_new = (
                                cal_each_augmented_cost(new_tour_a, depot, distance_matrix, param_lambda, penalty)
                                + cal_each_augmented_cost(new_tour_b, depot, distance_matrix, param_lambda, penalty))
                    augmented_cost_gain = augmented_cost_old - augmented_cost_new  # the more the better
                    if max_augmented_cost_gain >= augmented_cost_gain:
                        continue
                    cost_old = (cal_each_route_cost(tour_a, depot, distance_matrix) +
                                cal_each_route_cost(tour_b, depot, distance_matrix))
                    cost_new = (cal_each_route_cost(new_tour_a, depot, distance_matrix) +
                                cal_each_route_cost(new_tour_b, depot, distance_matrix))
                    cost_gain = cost_old - cost_new
                    # update
                    max_augmented_cost_gain = augmented_cost_gain
                    max_cost_gain = cost_gain
                    max_new_tour_a = [index_a, new_tour_a[:]]
                    max_new_tour_b = [index_b, new_tour_b[:]]
                    exchange_feasible = True
    if max_augmented_cost_gain < 1e-6:
        max_augmented_cost_gain = -float('inf')
        max_cost_gain = -float('inf')
        max_new_tour_a = None
        max_new_tour_b = None
        exchange_feasible = False

    return max_augmented_cost_gain, max_cost_gain, max_new_tour_a, max_new_tour_b, exchange_feasible


def neighbor_two_opt(vehicle_tours, customers, vehicle_capacity, distance_matrix, penalty, param_lambda):
    """
    local search: 2-opt
    """
    max_augmented_cost_gain = -float('inf')
    for index, tour in enumerate(vehicle_tours):
        opt_tour = tour[:]
        depot = customers[0]
        opt_tour.insert(0, depot)
        tour_length = len(opt_tour)
        for pos1, node1 in enumerate(opt_tour):
            pos2 = (pos1 + 1) % tour_length
            for pos3, node3 in enumerate(opt_tour):
                pos4 = (pos3 + 1) % tour_length
                if pos1 == pos3 or pos1 == pos4 or pos2 == pos3 or pos2 == pos4:
                    continue
                tour_new = list()
                tour_new.append(opt_tour[pos1])
                # swap
                if pos1 < pos3:
                    for node in opt_tour[pos3:pos1:-1]:
                        tour_new.append(node)
                else:
                    for node in opt_tour[pos3::-1] + opt_tour[-1:pos1:-1]:
                        tour_new.append(node)
                if pos1 < pos4:
                    for node in opt_tour[pos4:] + opt_tour[:pos1]:
                        tour_new.append(node)
                else:
                    for node in opt_tour[pos4:pos1]:
                        tour_new.append(node)
                # adjust route start form depot
                tour_adjust_new = list()
                for pos, node in enumerate(tour_new):
                    if node.index == 0:
                        start_pos = pos
                        break
                tour_adjust_new = tour_new[start_pos:] + tour_new[:start_pos]
                # calculate the cost
                del tour_adjust_new[0]
                if vehicle_endurance != float('inf'):
                    # check the distance constraint
                    route_aa = [node[0] for node in tour_adjust_new]
                    route_aa = [0] + route_aa + [0]
                    dt = sum(distance_matrix[i][j] for i, j in zip(route_aa[:-1], route_aa[1:]))
                    if dt + (len(tour_adjust_new) - 2) * service_time > vehicle_endurance:
                        continue
                augmented_cost_old = cal_each_augmented_cost(tour, depot, distance_matrix, param_lambda, penalty)
                augmented_cost_new = cal_each_augmented_cost(tour_adjust_new, depot, distance_matrix, param_lambda,
                                                             penalty)
                augmented_cost_gain = augmented_cost_old - augmented_cost_new
                if max_augmented_cost_gain >= augmented_cost_gain:
                    continue
                cost_old = cal_each_route_cost(tour, depot, distance_matrix)
                cost_new = cal_each_route_cost(tour_adjust_new, depot, distance_matrix)
                cost_gain = cost_old - cost_new
                max_augmented_cost_gain = augmented_cost_gain
                max_cost_gain = cost_gain
                max_tour_new = [index, tour_adjust_new[:]]
                two_opt_feasible = True
    if max_augmented_cost_gain < 1e-6:
        max_augmented_cost_gain = -float('inf')
        max_cost_gain = -float('inf')
        max_tour_new = None
        two_opt_feasible = False
    return max_augmented_cost_gain, max_cost_gain, max_tour_new, two_opt_feasible


def neighbor_cross(vehicle_tours, customers, vehicle_capacity, distance_matrix, penalty, param_lambda):
    """
    local search: cross
    """
    max_augmented_cost_gain = -float('inf')
    depot = customers[0]
    for index_a, tour_a in enumerate(vehicle_tours):
        for index_b, tour_b in enumerate(vehicle_tours):
            if tour_a == tour_b:
                continue
            new_tour_a, new_tour_b = list(), list()
            for pos_a, node_a in enumerate(tour_a[:]):
                for pos_b, node_b in enumerate(tour_b[:]):
                    demand_a = sum([i.demand for i in tour_a[pos_a:]])
                    a_available = vehicle_capacity - sum([i.demand for i in tour_a[:]])
                    demand_b = sum([i.demand for i in tour_b[pos_b:]])
                    b_available = vehicle_capacity - sum([i.demand for i in tour_b[:]])
                    if a_available + demand_a < demand_b:
                        continue
                    if b_available + demand_b < demand_a:
                        continue
                    new_tour_a = tour_a[:pos_a] + tour_b[pos_b:]
                    new_tour_b = tour_b[:pos_b] + tour_a[pos_a:]

                    if vehicle_endurance != float('inf'):
                        involve_constraint = False
                        # check two new route distance constraint:
                        for new_tour in [new_tour_a, new_tour_b]:
                            check_route = list()
                            for node in new_tour:
                                check_route.append(node[0])
                            rt, dt = opt_new_route(check_route)
                            if dt+(len(rt)-2)*service_time > vehicle_endurance:
                                involve_constraint = True
                                break
                        if involve_constraint:
                            continue

                    augmented_cost_old = (cal_each_augmented_cost(tour_a, depot, distance_matrix, param_lambda, penalty)
                                          + cal_each_augmented_cost(tour_b, depot, distance_matrix, param_lambda,
                                                                    penalty))
                    augmented_cost_new = (
                                cal_each_augmented_cost(new_tour_a, depot, distance_matrix, param_lambda, penalty)
                                + cal_each_augmented_cost(new_tour_b, depot, distance_matrix, param_lambda, penalty))
                    augmented_cost_gain = augmented_cost_old - augmented_cost_new
                    if max_augmented_cost_gain >= augmented_cost_gain:
                        continue
                    cost_old = (cal_each_route_cost(tour_a, depot, distance_matrix) +
                                cal_each_route_cost(tour_b, depot, distance_matrix))
                    cost_new = (cal_each_route_cost(new_tour_a, depot, distance_matrix) +
                                cal_each_route_cost(new_tour_b, depot, distance_matrix))
                    cost_gain = cost_old - cost_new
                    # update
                    max_augmented_cost_gain = augmented_cost_gain
                    max_cost_gain = cost_gain
                    max_new_tour_a = [index_a, new_tour_a[:]]
                    max_new_tour_b = [index_b, new_tour_b[:]]
                    cross_feasible = True
    if max_augmented_cost_gain < 1e-6:
        max_augmented_cost_gain = -float('inf')
        max_cost_gain = -float('inf')
        max_new_tour_a = None
        max_new_tour_b = None
        cross_feasible = False
    return max_augmented_cost_gain, max_cost_gain, max_new_tour_a, max_new_tour_b, cross_feasible


def init_lambda(cost, vehicle_tours, alpha):
    edge_count = 0
    for tour in vehicle_tours:
        if sum([i.demand for i in tour]) == 0:
            continue
        edge_count += len(tour) + 1
    return alpha * cost / edge_count


def add_penalty(penalty, vehicle_tours, distance_matrix, param_lambda, augmented_cost):
    max_util = -float('inf')
    max_edge = list()
    for tour in vehicle_tours:
        tour_node = [0] + [i.index for i in tour] + [0]
        for node_i, node_j in zip(tour_node[:-1], tour_node[1:]):
            util = distance_matrix[node_i][node_j] / (1 + penalty[node_i][node_j])
            if max_util < util:
                max_util = util
                max_edge = [[node_i, node_j]]
            elif max_util == util:
                max_edge.append([node_i, node_j])
    for edge in max_edge:
        penalty[edge[0]][edge[1]] += 10
        penalty[edge[1]][edge[0]] += 10
        augmented_cost += param_lambda
    return penalty, augmented_cost


def save_result(file_name, cost, tours):
    """
    write the solution into the txt.
    """
    with open(file_name, 'w') as f:
        f.write("%.3f %d\n" % (cost, 0))
        for tour in tours:
            f.write('0 ')
            for node in tour:
                f.write("%d " % node.index)
            f.write('0\n')


def show_result(all_routes, coordinates):
    """
    plot the graph
    """
    for index, route in enumerate(all_routes):
        x = []
        y = []
        for j in route:
            x.append(coordinates[j][0])
            y.append(coordinates[j][1])
            # random_color = [i[0] for i in np.random.rand(3, 1)]
            plt.scatter(x, y, c='r', marker="*")
            plt.plot(x, y, c='g')
    # depot
    z = []
    w = []
    z.append(coordinates[0][0])
    w.append(coordinates[0][1])
    for index in range(len(coordinates)):
        plt.text(coordinates[index][0], coordinates[index][1], index)
    plt.scatter(z, w, s=100, c="r", marker="o", label="Depot")
    plt.xlabel('City x coordinate')
    plt.ylabel("City y coordinate")
    plt.title("The VRP map by guided locate search")
    plt.legend()
    plt.show()


def print_result(all_route, distance_mat, demand):
    """
    print the result
    """
    total_distance = 0
    for num, route in enumerate(all_route):
        route_distance = sum([distance_mat[i][j] for i, j in zip(route[:-1], route[1:])])
        route_demand = sum([demand[i] for i in route])
        total_distance += route_distance
        print('Route %d - %.03f - %d : %s' % (num+1, route_distance, route_demand, route))
    print('The total distance: %.03f' % total_distance)


def guided_local_search(customers, depot, vehicle_capacity, vehicle_endurance, service_time, distance_matrix, iteration=500):
    """
    explore the optimal solution by GLS
    """
    customer_count = len(customers)
    # --- initial the route --- #
    vehicle_tours_dic, distance_dic = initial_routes(customers, depot)
    vehicle_tours = list()
    tour = list()
    # change the nametuple
    for r in vehicle_tours_dic.values():
        for node in r[1:-1]:
            tour.append(customers[node])
        vehicle_tours.append(tour[:])
        tour.clear()
    # show_result(vehicle_tours, coordinates)
    # print(vehicle_tours)
    # input('123')
    route_count = len(vehicle_tours)
    # --- calculate the cost of the solution; for each vehicle the length of the route --- #
    cost = cal_route_cost(route_count, vehicle_tours, depot, distance_matrix)
    # --- calculate augmented cost --- #
    param_lambda = 0.0
    alpha = 0.1
    penalty = np.zeros([customer_count, customer_count])
    augmented_cost = cal_route_augmented_cost(route_count, vehicle_tours, depot, distance_matrix,
                                              param_lambda, penalty)
    # --- current best solution --- #
    best_cost = cost
    best_tours = vehicle_tours
    step_limit = iteration

    # running local search ...
    for step in range(step_limit):
        print("Step: %s / %s, lambda: %s, cost & augmented_cost: %.3f & %.3f, best_cost: %.3f"
              % (step + 1, step_limit, param_lambda, cost, augmented_cost, best_cost))
        # --1-- relocate
        relocate_augmented_cost_gain, relocate_cost_gain, relocate_new_tour_a, relocate_new_tour_b, relocate_feasible = \
            neighbor_relocate(vehicle_tours, customers, vehicle_capacity, distance_matrix, penalty, param_lambda)
        # --2-- exchange
        exchange_augmented_cost_gain, exchange_cost_gain, exchange_new_tour_a, exchange_new_tour_b, exchange_feasible = \
            neighbor_exchange(vehicle_tours, customers, vehicle_capacity, distance_matrix, penalty, param_lambda)
        # --3-- 2-opt
        two_opt_augmented_cost_gain, two_opt_cost_gain, two_opt_vehicle_new, two_opt_feasible = \
            neighbor_two_opt(vehicle_tours, customers, vehicle_capacity, distance_matrix, penalty, param_lambda)
        # --4-- cross
        cross_augmented_cost_gain, cross_cost_gain, cross_new_tour_a, cross_new_tour_b, cross_feasible = \
            neighbor_cross(vehicle_tours, customers, vehicle_capacity, distance_matrix, penalty, param_lambda)
        # --- update the solution --- #
        if not relocate_feasible and not exchange_feasible and not two_opt_feasible and not cross_feasible:
            if param_lambda == 0.0:
                param_lambda = init_lambda(cost, vehicle_tours, alpha)
            penalty, augmented_cost = add_penalty(penalty, vehicle_tours, distance_matrix, param_lambda, augmented_cost)
        elif (relocate_augmented_cost_gain >= exchange_augmented_cost_gain and
              relocate_augmented_cost_gain >= two_opt_augmented_cost_gain and
              relocate_augmented_cost_gain >= cross_augmented_cost_gain):
            augmented_cost -= relocate_augmented_cost_gain
            cost -= relocate_cost_gain
            # change the new route
            index_a, index_b = relocate_new_tour_a[0], relocate_new_tour_b[0]
            tour_a, tour_b = relocate_new_tour_a[1][:], relocate_new_tour_b[1][:]
            vehicle_tours[index_a] = tour_a
            vehicle_tours[index_b] = tour_b
        elif (exchange_augmented_cost_gain >= relocate_augmented_cost_gain and
              exchange_augmented_cost_gain >= two_opt_augmented_cost_gain and
              exchange_augmented_cost_gain >= cross_augmented_cost_gain):
            augmented_cost -= exchange_augmented_cost_gain
            cost -= exchange_cost_gain
            # change the new route
            index_a, index_b = exchange_new_tour_a[0], exchange_new_tour_b[0]
            tour_a, tour_b = exchange_new_tour_a[1][:], exchange_new_tour_b[1][:]
            vehicle_tours[index_a] = tour_a
            vehicle_tours[index_b] = tour_b
        elif (two_opt_augmented_cost_gain >= relocate_augmented_cost_gain and
              two_opt_augmented_cost_gain >= exchange_augmented_cost_gain and
              two_opt_augmented_cost_gain >= cross_augmented_cost_gain):
            augmented_cost -= two_opt_augmented_cost_gain
            cost -= two_opt_cost_gain
            index, tour = two_opt_vehicle_new[0], two_opt_vehicle_new[1]
            vehicle_tours[index] = tour
        else:
            augmented_cost -= cross_augmented_cost_gain
            cost -= cross_cost_gain
            # change the new route
            index_a, index_b = cross_new_tour_a[0], cross_new_tour_b[0]
            tour_a, tour_b = cross_new_tour_a[1][:], cross_new_tour_b[1][:]
            vehicle_tours[index_a] = tour_a
            vehicle_tours[index_b] = tour_b
        # update the best solution
        if best_cost > cost:
            best_cost = cost
            best_tours = vehicle_tours[:]
            save_result("best_solution.txt", best_cost, best_tours)

    solution = list()
    for tour in best_tours:
        route = [0] + [i.index for i in tour] + [0]
        solution.append(route)
    return solution


if __name__ == '__main__':
    import os
    BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'data\Christofides1979\CMT1.vrp')
    # --- for different data
    pos = file_name.find('data')
    data_name = file_name[pos+5:pos+10]
    if data_name == 'Chris':
        customers, depot, vehicle_capacity, vehicle_endurance, service_time, coordinates, distance_matrix = import_Chris.init_data(file_name)
        demand_list = [c.demand for c in customers]  # all customer demand
    start_time = time.time()
    result = guided_local_search(customers, depot, vehicle_capacity, vehicle_endurance, service_time, distance_matrix, iteration=100)
    print('Running time:', time.time() - start_time)
    # --- show the result -- #
    print_result(result, distance_matrix, demand_list)
    show_result(result, coordinates)


    # instance
    # 'data\Christofides1979\CMT1.vrp'





