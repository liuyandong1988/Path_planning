#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/25 3:03
# test the vrp by Genetic Algorithm distance initialization
# data: Auger the capacity constraint
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
    depot_position = list()
    all_routes = list()
    route_dic = dict()
    for index, node in enumerate(solution):
        if node.index == 0:
            depot_position.append(index)

    for i, j in zip(depot_position[:-1], depot_position[1:]):
        all_routes.append(solution[i:j + 1])

    for num, route in enumerate(all_routes):
        one_route = list()
        demand = 0
        for c in route:
            one_route.append(c.index)
            demand += c.demand
        print('Route %s -- Demand %s : %s' %(num+1, demand, one_route))
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
    plt.title("The VRPTW map by GA")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    import os
    BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'data\Solomon_25\C101.25.txt')
    customers, depot, demand_list, vehicle_capacity, coordinates, distance_matrix = import_Solomon.init_data(file_name)
    # --- initialization population --- #
    population_size = 200
    population = vrptw_ga.initial_population(customers, depot, demand_list, population_size, distance_matrix, vehicle_capacity)
    # --- sort population by the fit function --- #
    vrptw_ga.sort_population(population)
    # --- iteration optimization --- #
    start_time = time.time()
    iteration = 0  # the iteration
    best_fitness = population[0].fitness
    best_individual = population[0]
    result_stop = 0
    while True:
        population = vrptw_ga.genetic_algorithm(population, population_size, depot, demand_list, vehicle_capacity)
        iteration += 1
        print('Gen ', iteration)
        pop_info(population)
        print('-----------------')
        # the current generate fitness
        current_fitness = population[0].fitness
        if current_fitness > best_fitness:
            best_individual = population[0]
            best_fitness = current_fitness
        elif current_fitness == current_fitness:
            result_stop += 1
        if result_stop == 10:
            break
    print('Running time: ', time.time() - start_time)
    # --- print the best solution --- #
    route_dic = print_solution(best_individual.data)
    total_distance = 0
    for key, val in route_dic.items():
        total_distance += sum([distance_matrix[i][j] for i, j in zip(val[:-1], val[1:])])
    print('The total distance %.01f' % total_distance)
    show_result(route_dic, coordinates)




    # instance
    # data\Solomon_25\C101.25.txt
    # R101.25.txt
