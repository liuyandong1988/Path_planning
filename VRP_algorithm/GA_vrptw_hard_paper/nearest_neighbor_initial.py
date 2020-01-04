#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/31 14:31
# hard vrptw nearest neighbor

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/25 3:03
# test the vrp by Genetic Algorithm distance initialization
# data: Solomon hard vrptw
import import_Solomon
import vrptw_ga
import matplotlib.pyplot as plt
import time


def pop_info(population):
    """
    calculate the average fitness
    :param population:
    :return:
    """
    min_fitness = population[0].fitness
    avg_fitness = 0
    for i in range(len(population)):
        avg_fitness += population[i].fitness
    avg_fitness /= len(population)
    print('Avg Fit:', avg_fitness)
    print('Min Fit:', min_fitness)


def print_solution(solution):
    route_dic = dict()
    total_distance = 0
    for num, route in solution.items():
        one_route = list()
        part_demand = 0
        for c in route:
            one_route.append(c.index)
            part_demand += c.demand
        part_distance = sum([distance_matrix[i][j] for i,j in zip(one_route[:-1], one_route[1:])])
        print('Route %s -- Demand: %d  : %s' %(num, part_demand, one_route))
        route_dic[num] = one_route
        total_distance += part_distance
    print('The total distance: %.03f' % total_distance)

    return route_dic




def show_result(all_routes, coordinates):
    """
    plot the graph
    """
    for index, route in all_routes.items():
        x = []
        y = []
        for j in route:
            x.append(coordinates[j.index][0])
            y.append(coordinates[j.index][1])
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
    plt.title("The VRPTW map by NN")
    plt.legend()
    plt.show()



def check_tw(part_route, next_node, distance_matrix):
    """
    Check the customer time window
    """
    total_travel_time = 0
    if len(part_route) != 1:
        for ind, node in enumerate(part_route):
            if ind == 0:
                continue
            else:
                last_node = part_route[ind-1]
                t_ij = distance_matrix[last_node.index][node.index]
                if ind == 1 and t_ij < node.start:
                    total_travel_time += (node.start + node.service)
                else:
                    total_travel_time += (t_ij + node.service)
    check_time_window = total_travel_time + distance_matrix[part_route[-1].index][next_node.index]
    if len(part_route) == 1 and check_time_window < next_node.start:
        check_time_window = next_node.start

    if next_node.start <= check_time_window <= next_node.end:
        total_travel_time = check_time_window
        total_travel_time += next_node.service
        return True, total_travel_time
    else:
        return False, None


def check_return_depot_time(total_route, depot, distance_matrix):
    """
    The return time must be in the depot end time
    """
    total_time = 0
    for ind, node in enumerate(total_route):
        if ind==0:
            continue
        else:
            last_node = total_route[ind-1]
            t_ij = distance_matrix[last_node.index][node.index]
            total_time += (t_ij+node.service)
    if total_time <= depot.end:
        return True
    else:
        return False


def check_vehcile_capacity(part_route, vehicle_capacity):
    """
    check the capacity constraint
    """
    total_demand = 0
    for customer in part_route:
        total_demand += customer.demand
    if total_demand <= vehicle_capacity:
        return True
    else:
        return False


def find_route_reset(solution, route_id, part_route, last_node, nn_allow_nodes, depot, remain_nodes):
    """
    reset the variables
    """
    part_route.append(depot)
    solution[route_id] = part_route
    route_id += 1
    part_route = [depot]
    last_node = depot
    nn_allow_nodes = remain_nodes[:]
    return solution, route_id, part_route, last_node, nn_allow_nodes

def nearest_neighbor(genes, depot, distance_matrix, vehicle_capacity):
    """
    sort the costumers by nearest neighbor
    the route excludes the depot
    """
    remain_nodes = genes[:]
    last_node = depot
    visited_nodes = [depot]
    part_route = [depot]
    solution = dict()
    route_id = 1
    nn_allow_nodes = remain_nodes[:]
    while remain_nodes:
        # find the nearest next node
        min_distance = float('inf')
        for j in nn_allow_nodes:
            curr_distance = distance_matrix[last_node.index][j.index]
            if curr_distance < min_distance:
                next_node = j
                min_distance = curr_distance
        # check the time window
        ctw_mark, part_distance = check_tw(part_route, next_node, distance_matrix)
        if ctw_mark:
            # check the return depot time
            crdt_mark = check_return_depot_time(part_route, depot, distance_matrix)
            if crdt_mark:
                # check the capacity constraint
                cvc_mark = check_vehcile_capacity(part_route, vehicle_capacity)
                if cvc_mark:
                    # satisfy all constraints and add the node to route
                    part_route.append(next_node)
                    last_node = next_node
                    remain_nodes.remove(next_node)
                    nn_allow_nodes = remain_nodes[:]
                else:
                    # the next node cannot satisfy capacity constraint
                    nn_allow_nodes.remove(next_node)
                    if nn_allow_nodes == []:
                        # create a new route and reset the variables
                        solution, route_id, part_route, last_node, nn_allow_nodes = \
                            find_route_reset(solution, route_id, part_route, last_node, nn_allow_nodes, depot, remain_nodes)
            else:
                # cannot satisfy return depot constraint
                nn_allow_nodes.remove(next_node)
                if nn_allow_nodes == []:
                    # create a new route and reset the variables
                    solution, route_id, part_route, last_node, nn_allow_nodes = \
                        find_route_reset(solution, route_id, part_route, last_node, nn_allow_nodes, depot, remain_nodes)
        else:
            # cannot satisfy time window
            nn_allow_nodes.remove(next_node)
            if nn_allow_nodes == []:
                # create a new route and reset the variables
                solution, route_id, part_route, last_node, nn_allow_nodes = \
                    find_route_reset(solution, route_id, part_route, last_node, nn_allow_nodes, depot, remain_nodes)
    if len(part_route) > 1:
        # the remain route
        part_route.append(depot)
        solution[route_id] = part_route
        route_id += 1
    return solution

if __name__ == '__main__':
    import os
    BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'data\Solomon_25\C101.25.txt')
    customers, depot, demand_list, vehicle_capacity, coordinates, distance_matrix = import_Solomon.init_data(file_name)
    # --- initialization --- #
    solution = nearest_neighbor(customers, depot, distance_matrix, vehicle_capacity)
    print_solution(solution)
    show_result(solution, coordinates)


    # instance
    # data\Solomon_25\C101.25.txt
    # R101.25.txt
