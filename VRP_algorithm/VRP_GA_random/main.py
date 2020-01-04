#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/25 3:03
# test the vrp by Genetic Algorithm
# data: Christofides1979  include the capacity and distance constraints
import import_Chris
import node_property
import vrp_ga
import matplotlib.pyplot as plt
import time


def initial_node_property(customer_node, depot_node):
    """
    initial customer and depot property
    """
    # --- customer --- #
    customers = list()
    for n in customer_node:
        c_property = [n.index, n.x, n.y, service_time, n.demand]
        new_customer = node_property.Customer(*tuple(c_property))
        customers.append(new_customer)
    d_property = [depot_node.index, depot_node.x, depot_node.y, vehicle_endurance, vehicle_capacity, None]
    new_depot = node_property.Depot(*tuple(d_property))
    return customers, new_depot


def pop_info(population):
    """
    calculate the average fitness
    :param population:
    :return:
    """
    min_fitness = population[0].get_solution().total_distance
    avg_fitness = 0
    for i in range(len(population)):
        avg_fitness += population[i].get_solution().total_distance
    avg_fitness /= len(population)
    print('Avg Fit:', avg_fitness)
    print('Min Fit:', min_fitness)


def print_solution(solution, cost):
    route_dic = dict()
    print('The best solution cost: %.03f' % cost)
    for num, route in enumerate(solution):
        one_route = list()
        for c in route:
            one_route.append(c.id)
        print('Route %s : %s' %(num+1, one_route))
        route_dic[num] = one_route
    return route_dic

def show_result(all_routes, coordinates):
    """
    plot the graph
    """
    for index, route in all_routes.items():
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
    plt.title("The VRP map by GA")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    import os
    BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'data\Christofides1979\CMT1.vrp')
    # --- for different data
    pos = file_name.find('data')
    data_name = file_name[pos + 5:pos + 10]
    if data_name == 'Chris':
        customers, depot, vehicle_capacity, vehicle_endurance, service_time, coordinates, distance_matrix = import_Chris.init_data(file_name)
    # --- instantiation customer and depot --- #
    customers, depot = initial_node_property(customers[1:], depot)
    # --- initialization solutions --- #
    population_size = 500
    population = vrp_ga.initial_population(customers, depot, population_size)
    # --- sort population by the fit function --- #
    vrp_ga.sort_population(population)
    # --- iteration optimization --- #
    iteration = 100
    start_time = time.time()
    for i in range(iteration):
        population = vrp_ga.genetic_algorithm(population, population_size, depot)
        print('Gen ', i+1)
        pop_info(population)
        print('-----------------')
    print('Running time: ', time.time()-start_time)
    # --- print the best solution --- #
    best_solution = population[0].get_solution().tours
    min_cost = population[0].get_solution().total_distance
    route_dic = print_solution(best_solution, min_cost)
    show_result(route_dic, coordinates)




    # # instance
    # # 'data\Augerat1995\A-n32-k5.vrp'
    # # A-n32-k5.vrp
    # # A-n33-k5.vrp
    # # A-n33-k6.vrp
    # # A-n45-k7.vrp
    # # A-n65-k9.vrp
    # # A-n80-k10.vrp
    # iteration = 2
    # pop_size = 300
    # customers, depots = getProblemSet(p23)
    # population = initialPopulation(customers, depots, pop_size)
    # sortPop(population)
    # for i in range(iteration):
    #     population = geneticAlgorithm(population, pop_size)
    #     print('Gen ', i + 1)
    #     pop_info(population)
    #     print('-----------------')
    # population[0].get_solution().write_to_file()
    # population[0].get_solution().plot()