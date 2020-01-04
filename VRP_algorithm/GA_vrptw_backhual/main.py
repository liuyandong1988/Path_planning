#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/25 3:03
# VRP with backhauling, first delivery all goods to customer and then pickup the goods to return the depot
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
    for num, route in enumerate(solution):
        one_route = list()
        part_demand = 0
        for c in route:
            one_route.append(c.index)
            # part_demand += c.demand
        part_distance = sum([distance_matrix[i][j] for i,j in zip(one_route[:-1], one_route[1:])])
        print('Route %s -- Demand: %d  : %s' %(num+1, part_demand, one_route))
        route_dic[num] = one_route
        total_distance += part_distance
    print('The total distance: %.03f' % total_distance)

    return route_dic


def show_result(all_routes):
    """
    plot the graph
    """
    for index, route in enumerate(all_routes):
        x = []
        y = []
        color = []
        for j in route:
            x.append(coordinates[j.index][0])
            y.append(coordinates[j.index][1])
            if j.pd_mark == 0:
                color.append('r')
            else:
                color.append('g')
            # random_color = [i[0] for i in np.random.rand(3, 1)]
        plt.scatter(x, y, c=color, marker="o", s=50)
        plt.plot(x, y, c='g')
    # depot
    z = []
    w = []
    z.append(coordinates[0][0])
    w.append(coordinates[0][1])
    for index in range(len(coordinates)):
        plt.text(coordinates[index][0], coordinates[index][1], index)
    plt.scatter(z, w, s=100, c="black", marker="*", label="Depot")
    plt.xlabel('City x coordinate')
    plt.ylabel("City y coordinate")
    plt.title("The VRPTW map by GA")
    plt.legend()
    plt.show()


def show_customer(nodes):
    c_red_green = ['black']
    x, y = list(), list()
    x.append(coordinates[0][0])
    y.append(coordinates[0][1])
    for n in nodes:
        if n.pd_mark == 1:
            c_red_green.append('r')
        else:
            c_red_green.append('g')
        x.append(n.x)
        y.append(n.y)
    plt.scatter(x, y, s=100, c=c_red_green, marker="o", label="Depot")
    plt.show()




if __name__ == '__main__':
    import os
    BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'data\Solomon_25\R101.25.txt')
    customers, depot, demand_list, vehicle_capacity, coordinates, distance_matrix = import_Solomon.init_data(file_name)
    delivery_c, pickup_c = list(), list()
    for i in customers:
        if i.pd_mark == 1:
            delivery_c.append(i)  # the delivery customer
        else:
            pickup_c.append(i)  # the pickup customer
    # show_customer(customers)
    # --- initialization population --- #
    population_size = 100
    population = vrptw_ga.initial_population(delivery_c, pickup_c, depot, distance_matrix, vehicle_capacity, population_size)
    # show_result(population[0].feasible_solution)
    # --- sort population by the fit function --- #
    vrptw_ga.sort_population(population)
    # --- iteration optimization --- #
    iteration = 500
    start_time = time.time()
    for i in range(iteration):
        population = vrptw_ga.genetic_algorithm(population, depot, demand_list, vehicle_capacity, distance_matrix, coordinates, population_size)
        print('Gen ', i+1)
        pop_info(population)
        print('-----------------')
        # print_solution(population[0].feasible_solution)
        # show_result(population[0].feasible_solution)
    print('Running time: ', time.time()-start_time)
    # --- print the best solution --- #
    best_solution = population[0].feasible_solution
    print_solution(best_solution)
    show_result(best_solution)





    # instance
    # data\Solomon_25\C101.25.txt
    # R101.25.txt
