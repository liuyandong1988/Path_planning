#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/17 11:38
# solve the tsp by 3-optimal
# http://tsp-basics.blogspot.com/2017/03/3-opt-move.html

# from r_optimal import import_data
from matplotlib import pyplot as plt


def gain_from_three_optimal(X1, X2, Y1, Y2, Z1, Z2, optimal_case, distance_matrix):
    """
    Find the best case form the 8 different cases
    :return:
    """
    if optimal_case == 'opt3_case_0':
        return 0, optimal_case
    elif optimal_case == 'opt3_case_1':
        del_length = distance_matrix[X1][X2] + distance_matrix[Z1][Z2]
        add_length = distance_matrix[X1][Z1] + distance_matrix[X2][Z2]
    elif optimal_case == 'opt3_case_2':
        del_length = distance_matrix[Y1][Y2] + distance_matrix[Z1][Z2]
        add_length = distance_matrix[Y1][Z1] + distance_matrix[Y2][Z2]
    elif optimal_case == 'opt3_case_3':
        del_length = distance_matrix[X1][X2] + distance_matrix[Y1][Y2]
        add_length = distance_matrix[X1][Y1] + distance_matrix[X2][Y2]
    elif optimal_case == 'opt3_case_4':
        add_length = distance_matrix[X1][Y1] + distance_matrix[X2][Z1] + distance_matrix[Y2][Z2]
    elif optimal_case == 'opt3_case_5':
        add_length = distance_matrix[X1][Z1] + distance_matrix[Y2][X2] + distance_matrix[Y1][Z2]
    elif optimal_case == 'opt3_case_6':
        add_length = distance_matrix[X1][Y2] + distance_matrix[Z1][Y1] + distance_matrix[X2][Z2]
    elif optimal_case == 'opt3_case_7':
        add_length = distance_matrix[X1][Y2] + distance_matrix[Z1][X2] + distance_matrix[Y1][Z2]
    if optimal_case in ['opt3_case_4', 'opt3_case_5', 'opt3_case_6', 'opt3_case_7']:
        del_length = distance_matrix[X1][X2] + distance_matrix[Y1][Y2] + distance_matrix[Z1][Z2]
    result = del_length - add_length
    return result, optimal_case


def reverse_segment(tour, index1, index2):
    city_num = len(tour)
    if index1 == city_num:
        return tour[index2]
    if index1 != 0:
        index1_1 = index1 - 1
    else:
        index1_1 = index1
    if index1 < index2:
        reverse_part = tour[index2:index1_1:-1]
        if index1 == 0:
            reverse_part.append(tour[0])
    else:
        reverse_part = tour[index2::-1] + tour[:index1_1:-1]
    return reverse_part


def make_three_optimal_move(tour, nodes, opt_case):
    """
    exchange the city sequence
    :return:
    """
    i, j, k = nodes[0], nodes[1], nodes[2]
    city_num = len(tour)
    if k + 1 < i + 1:
        part1 = tour[k + 1:i + 1]
    else:
        part1 = tour[k + 1:] + tour[:i + 1]

    if i + 1 < j + 1:
        part2 = tour[i + 1:j + 1]
    else:
        part2 = tour[i + 1:] + tour[:j + 1]

    if j + 1 < k + 1:
        part3 = tour[j + 1:k + 1]
    else:
        part3 = tour[j + 1:] + tour[:k + 1]
    if opt_case == 'opt3_case_0':
        result_tour = tour
    # 2-OPT MOVES
    elif opt_case == 'opt3_case_1':  # a'bc
        reverse_part1 = reverse_segment(tour, (k + 1) % city_num, i)
        result_tour = reverse_part1 + part2 + part3
    elif opt_case == 'opt3_case_2':  # abc'
        reverse_part1 = reverse_segment(tour, (j + 1) % city_num, k)
        result_tour = part1 + part2 + reverse_part1
    elif opt_case == 'opt3_case_3':  # ab'c
        reverse_part1 = reverse_segment(tour, (i + 1) % city_num, j)
        result_tour = part1 + reverse_part1 + part3
    elif opt_case == 'opt3_case_4':  # ab'c'
        reverse_part1 = reverse_segment(tour, (i + 1) % city_num, j)
        reverse_part2 = reverse_segment(tour, (j + 1) % city_num, k)
        result_tour = part1 + reverse_part1 + reverse_part2
    elif opt_case == 'opt3_case_5':  # a'b'c
        reverse_part1 = reverse_segment(tour, (k + 1) % city_num, i)
        reverse_part2 = reverse_segment(tour, (i + 1) % city_num, j)
        result_tour = reverse_part1 + reverse_part2 + part3
    elif opt_case == 'opt3_case_6':  # a'bc'
        reverse_part1 = reverse_segment(tour, (k + 1) % city_num, i)
        reverse_part2 = reverse_segment(tour, (j + 1) % city_num, k)
        result_tour = reverse_part1 + part2 + reverse_part2
    elif opt_case == 'opt3_case_7':  # a'b'c'
        reverse_part1 = reverse_segment(tour, (k + 1) % city_num, i)
        reverse_part2 = reverse_segment(tour, (i + 1) % city_num, j)
        reverse_part3 = reverse_segment(tour, (j + 1) % city_num, k)
        result_tour = reverse_part1 + reverse_part2 + reverse_part3
    repeat_remove = []
    for city in result_tour:
        if city not in repeat_remove:
            repeat_remove.append(city)
    return repeat_remove

def three_optimal(route, distance_matrix):
    """
    tsp by 3-opt
    :param route: [0, ....]
    :param distance_matrix:
    :return: the best solution
    """
    local_optimal = False
    route_length = len(route)

    while not local_optimal:
        local_optimal = True
        best_cost = 0
        best_case = None
        for i in range(0, route_length):
            for j in range(0, route_length):
                for k in range(0, route_length):
                    if (k > j > i and k != j + 1 and j != i + 1 and i != k + 1) or \
                            (i > k > j and i != k + 1 and k != j + 1 and j != i + 1) or \
                            (j > i > k and j != i + 1 and i != k + 1 and k != j + 1):
                        X1 = route[i]
                        Y1 = route[j]
                        Z1 = route[k]
                        if (i + 1) % route_length == 0:
                            X2 = route[0]
                        else:
                            X2 = route[i + 1]
                        if (j + 1) % route_length == 0:
                            Y2 = route[0]
                        else:
                            Y2 = route[j + 1]
                        if (k + 1) % route_length == 0:
                            Z2 = route[0]
                        else:
                            Z2 = route[k + 1]
                        # different exchange case
                        eight_case = ['opt3_case_0', 'opt3_case_1', 'opt3_case_2', 'opt3_case_3',
                                      'opt3_case_4', 'opt3_case_5', 'opt3_case_6', 'opt3_case_7']
                        for case in eight_case:
                            gain_cost, current_case = gain_from_three_optimal(X1, X2, Y1, Y2, Z1, Z2, case, distance_matrix)  # if distance matrix excludes 0 node minus 1
                            if gain_cost > best_cost:
                                best_cost = gain_cost
                                best_case = current_case
                                local_optimal = False
                                nodes = [i, j, k]
                                # print(best_case, best_cost)
        if not local_optimal:
            route = make_three_optimal_move(route, nodes, best_case)
    result = route[route.index(0):] + route[:route.index(0)]
    return result


def calculate_cost(route, distance_matrix):
    """
    calculate the cost of route
    :param route:
    :param distance_matrix:
    :return:
    """
    total_cost = 0
    for city_1, city_2 in zip(route[:-1], route[1:]):
        total_cost += distance_matrix[city_1-1][city_2-1]
    return total_cost


# --- draw the result --- #
def show_result(city_solution, city_coordinate):
    x_coordinate = []
    y_coordinate = []
    # draw the result
    for city in city_solution:
        x_coordinate.append(city_coordinate[city-1][0])
        y_coordinate.append(city_coordinate[city-1][1])
    plt.figure(1)
    plt.scatter(x_coordinate,y_coordinate)
    plt.plot(x_coordinate,y_coordinate)
    # draw the city mark
    for city in city_solution:
        plt.text(city_coordinate[city-1][0], city_coordinate[city-1][1], city)
    # plt.text(city_coordinate[city_solution[0]-1][0], city_coordinate[city_solution[0]-1][1], 'Start')   #start
    # plt.text(city_coordinate[city_solution[-1]-1][0], city_coordinate[city_solution[-1]-1][1], '          End')   #end
    plt.xlabel('City x coordinate')
    plt.ylabel("City y coordinate")
    plt.title("The traveling map by 3_opt")
    plt.grid()
    plt.show()

if __name__ == '__main__':
    import os, random
    BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'eil51.tsp')
    coordinates, distance_matrix, city_number = import_data.init_data(file_name)
    # initial route
    initial_route = list(range(1, city_number+1))
    # initial_route = list(range(1, 10))
    random.shuffle(initial_route)
    solution = three_optimal(initial_route, distance_matrix)
    total_distance = calculate_cost(solution, distance_matrix)
    print('The traveling total distance: %s' % total_distance)
    print('The route:', solution)
    show_result(solution, coordinates)



