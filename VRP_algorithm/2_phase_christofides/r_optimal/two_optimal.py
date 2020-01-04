#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/17 8:14
# solve the tsp by 2-optimal
# http://pedrohfsd.com/2017/08/09/2opt-part1.html

from r_optimal import import_data
from matplotlib import pyplot as plt


def calculate_cost(route, distance_matrix):
    """
    calculate the cost of route
    :param route:
    :param distance_matrix:
    :return:
    """
    total_cost = 0
    for city_1, city_2 in zip(route[:-1], route[1:]):
        total_cost += distance_matrix[city_1][city_2]
    return total_cost


def two_opt(route, distance_matrix):
    """
    solve the TSP by two_opt
    :param route: [start_point, ..., end_point(the same as start_point)]
    :param distance_matrix: dij
    :return:
    """
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue  # changes nothing, skip then
                new_route = route[:]
                new_route[i:j] = route[j - 1:i - 1:-1]  # this is the 2-optSwap
                if calculate_cost(new_route, distance_matrix) < calculate_cost(best, distance_matrix):
                    best = new_route
                    improved = True
        route = best
    return best

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
    plt.title("The traveling map by 2_opt")
    plt.grid()
    plt.show()



if __name__ == '__main__':
    import os, random
    BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'eil51.tsp')
    coordinates, distance_matrix, city_number = import_data.init_data(file_name)
    # initial route
    initial_route = list(range(1, city_number+1))
    # initial_route = list(range(1, 6))
    random.shuffle(initial_route)
    initial_route.append(initial_route[0])
    # print(initial_route)
    solution = two_opt(initial_route, distance_matrix)
    total_distance = calculate_cost(solution, distance_matrix)
    print('The traveling total distance: %s'%total_distance)
    print('The route:', solution)
    show_result(solution, coordinates)

