#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/18 1:06
# some support function

from matplotlib import pyplot as plt
import numpy as np

# ---  plot the graph  --- #
def show_result(all_routes, coordinates):
    for key, route in all_routes.items():
        x = []
        y = []
        # add depot as start and end point
        for j in route:
            x.append(coordinates[j][0])
            y.append(coordinates[j][1])
            random_color = [i[0] for i in np.random.rand(3, 1)]
            plt.scatter(x, y, c=random_color, marker="*")
            plt.plot(x, y, c=random_color)
    # depot
    z = []
    w = []
    z.append(coordinates[0][0])
    w.append(coordinates[0][1])
    for index in range(len(coordinates)):
        plt.text(coordinates[index][0], coordinates[index][1], index)
    plt.scatter(z, w, s=100, c="r", marker="o", label="Depot")
    plt.xlabel('City x coordinates')
    plt.ylabel("City y coordinates")
    plt.title("The VRP map by 2-phase")
    plt.legend()
    plt.show()


def show_route(city_solution, coordinates):
    """
    draw the result
    :param city_solution: have the depot (0)
    :param coordinates: 
    :return: 
    """
    x_coordinate = []
    y_coordinate = []
    # draw the result
    for city in city_solution:
        x_coordinate.append(coordinates[city][0])
        y_coordinate.append(coordinates[city][1])
    plt.figure(1)
    plt.scatter(x_coordinate,y_coordinate)
    plt.plot(x_coordinate,y_coordinate)
    # draw the city mark
    for city in city_solution:
        plt.text(coordinates[city][0], coordinates[city][1], city)
    # plt.text(coordinates[city_solution[0]][0], coordinates[city_solution[0]][1], 'Start')   #start
    # plt.text(coordinates[city_solution[-1]][0], coordinates[city_solution[-1]][1], '          End')   #end
    plt.xlabel('City x coordinate')
    plt.ylabel("City y coordinate")
    plt.title("The traveling map")
    plt.grid()
    plt.show()


def calculate_cost(route, distance_matrix):
    """
    calculate the cost of route
    :param route: the route includes the depot (0)
    :param distance_matrix:
    :return:
    """
    total_cost = 0
    for city_1, city_2 in zip(route[:-1], route[1:]):
        total_cost += distance_matrix[city_1][city_2]
    return total_cost