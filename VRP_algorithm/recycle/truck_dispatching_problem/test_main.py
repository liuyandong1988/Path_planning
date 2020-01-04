#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/14 13:13
# Description: ‘The truck dispatching problem’ by G. B. Dantzig 1959

import numpy as np
import import_data
import time, math, copy

def cal_aggregation_times(customers, vehicle_capacity):
    aggregation_times = 0
    aggre_time_capacity = dict()
    demand_nodes = [i.demand for i in customers[1:]]
    # sort in increased order
    demand_nodes.sort()
    loading_capacity = list()
    for i in demand_nodes:
        if sum(loading_capacity) + i > vehicle_capacity:
            break
        else:
            loading_capacity.append(i)
    aggregation_times = math.ceil(math.log(len(loading_capacity), 2))
    # print(loading_capacity, aggregation_times)
    for i in range(aggregation_times):
        aggre_time_capacity[i+1] = math.pow(0.5, aggregation_times-1-i) * vehicle_capacity
    # print(aggre_time_capacity)
    # input('123')
    return aggregation_times, aggre_time_capacity


def check_capacity(t1, t2, vehicle_capacity):
    nodes = list()
    total_capacity = 0
    for i in t1:
        nodes.append(i)
    for j in t2:
        nodes.append(j)
    for n in nodes:
        total_capacity += n.demand
    if total_capacity <= vehicle_capacity:
        return True
    else:
        return False

def merge_items(t1, t2, distance_matrix):
    print(t1, t2)
    merge_1 = list(t1) + list(t2)
    merge_2 = list(t1) + list(t2)[::-1]
    merge_3 = list(t2) + list(t1)
    merge_4 =


def linear_programming_search(customers, depot, vehicle_count, vehicle_capacity, coordinates, distance_matrix):
    """
    explore the optimal solution by linear research
    """
    basic_set = dict()
    # --- initial basic set --- #
    for i in customers[1:]:
        basic_set[(0, i.index)] = 1
    # print(basic_set)
    # --- aggregation times and capacity --- #
    aggregation_times, aggre_time_capacity = cal_aggregation_times(customers, vehicle_capacity)
    for times in range(aggregation_times):
        if times+1 == 1:
            group = list()
            visited = list()
            distance_compare = distance_matrix.copy()
            # --- the first time aggregation --- #
            while True:
                min_distance = float('inf')
                for i in range(1, len(distance_compare)):
                    for j in range(1, i):
                        tmp_distance = distance_compare[i][j]
                        if (tmp_distance < min_distance and
                                (customers[i].demand + customers[j].demand) <= aggre_time_capacity[times+1] and
                                i not in visited and j not in visited):
                            min_distance = tmp_distance
                            min_row = i
                            min_column = j
                distance_compare[min_row][min_column] = float('inf')
                if min_distance == float('inf'):
                    break
                # --- modify the basic set --- #
                if distance_compare[0][min_row] < distance_compare[0][min_column]:
                    del_item = (0, min_column)
                    modify_zero = (0, min_row)
                else:
                    del_item = (0, min_row)
                    modify_zero = (0, min_column)
                tmp_total_distance = 0
                # before distance
                for key, val in basic_set.items():
                    if val == 1:
                        tmp_total_distance += distance_matrix[key[0]][key[1]]
                # after distance
                modify_distance = 0
                modify_basic_set = copy.deepcopy(basic_set)
                del modify_basic_set[del_item]
                modify_basic_set[modify_zero] = 0
                modify_basic_set[(min_row, min_column)] = 1
                for key, val in modify_basic_set.items():
                    if val == 1:
                        modify_distance += distance_matrix[key[0]][key[1]]
                if modify_distance < tmp_total_distance:
                    del basic_set[del_item]
                    basic_set[modify_zero] = 0
                    basic_set[(min_row, min_column)] = 1
                    group.append((min_row, min_column))
                    visited.append(min_column)
                    visited.append(min_row)
            for i in customers[1:]:
                if i.index not in visited:
                    group.append((i.index,))
            print('00', group)
            # ---- other aggregation --- #
            new_group = list()
            for ind_1, item_1 in enumerate(group):
                for ind_2, item_2 in enumerate(group[ind_1+1:]):
                    if check_capacity(item_1, item_2, vehicle_capacity):
                        merge_items(item_1, item_2, distance_matrix)
                    print(item_1, item_2)
                    input('1')



            input('123')


    customer_count = len(customers)
    # --- initial the route --- #
    vehicle_tours = initial_routes(customers, depot, vehicle_count, vehicle_capacity)
    # --- calculate the cost of the solution; for each vehicle the length of the route --- #
    cost = cal_route_cost(vehicle_count, vehicle_tours, depot, distance_matrix)
    # --- calculate augmented cost --- #
    param_lambda = 0.0
    alpha = 0.1
    penalty = np.zeros([customer_count, customer_count])
    augmented_cost = cal_route_augmented_cost(vehicle_count, vehicle_tours, depot, distance_matrix,
                                              param_lambda, penalty)
    # --- current best solution --- #
    best_cost = cost
    best_tours = vehicle_tours
    step_limit = iteration
    start_time = time.time()
    # running local search ...
    for step in range(step_limit):
        print("Step: %s / %s, lambda: %s, cost & augmented_cost: %.3f & %.3f, best_cost: %.3f"
              % (step + 1, step_limit, param_lambda, cost, augmented_cost, best_cost))
        print('Running time:', time.time()-start_time)
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
    num = 0
    for tour in best_tours:
        num += 1
        route = [0] + [i.index for i in tour] + [0]
        solution.append(route)
        print('Route %d : %s' % (num, route))

    show_result(solution, coordinates)


if __name__ == '__main__':
    import os
    BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'data\A-n32-k5.vrp')
    customers, depot, vehicle_count, vehicle_capacity, coordinates, distance_matrix = import_data.read_data(file_name)

    linear_programming_search(customers, depot, vehicle_count, vehicle_capacity, coordinates, distance_matrix)



