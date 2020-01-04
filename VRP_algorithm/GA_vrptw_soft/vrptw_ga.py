#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/25 3:14
# initialization randomly !
# crossover, move the depot in the two route to optimize
# mutation, genes swap

import random, math
import matplotlib.pyplot as plt
from copy import deepcopy

class Chromosome(object):
    """Chromosome"""
    def __init__(self, genes, depot, demand_list, vehicle_capacity, data=None, waiting_penalty=0, delay_penalty=100):

        self.genes = genes
        self.depot = depot
        self.demand_list = demand_list
        self.waiting_penalty = waiting_penalty
        self.delay_penalty = delay_penalty
        self.vehicle_capacity = vehicle_capacity
        if data is None:
            self.data = self._generate_chromosome()
        else:
            self.data = data
        self.fitness = self.get_fitness()

    def _generate_chromosome(self):
        """
        generate the feasible solution based on vehicle capacity
        """
        sum_load = 0
        new_data = list()
        new_data.append(self.depot)
        for index, gene in enumerate(self.genes):
            sum_load += gene.demand
            if sum_load > self.vehicle_capacity:
                new_data.append(self.depot)
                sum_load = gene.demand
            new_data.append(gene)
        new_data.append(self.depot)
        return new_data

    def get_fitness(self):
        """
        calculate the fitness of solution
        :return:
        """
        fitness = 0
        dist_cost = 0
        time_cost = 0
        over_load_cost = 0
        part_distance = list()

        # calculate distance
        i = 1
        while i < len(self.data):
            cal_distance = lambda x1, y1, x2, y2: math.sqrt(math.pow(x1-x2, 2)+math.pow(y1-y2, 2))
            part_distance.append(cal_distance(self.data[i].x, self.data[i].y, self.data[i-1].x, self.data[i-1].y))
            i += 1
        dist_cost = sum(part_distance)

        # time cost: travel_time + penalty_cost + service_time
        time_spend = 0
        for ind, pos in enumerate(self.data):
            if pos.index == 0:
                time_spend = 0
            if ind != 0:
                # travel time
                time_spend += cal_distance(pos.x, pos.y, self.data[ind-1].x, self.data[ind-1].y)
                # arrive early
                if time_spend < pos.start:
                    time_cost += (pos.start-time_spend) * self.waiting_penalty
                # arrive late
                if time_spend > pos.end:
                    time_cost += (time_spend-pos.end) * self.delay_penalty
                # update the time service_time
                time_spend += pos.service
                time_cost += pos.service

        # over load
        load = 0
        for index, gene in enumerate(self.data):
            if index == 0:
                continue
            elif gene.index == 0:
                load = 0
            else:
                load += self.demand_list[gene.index]
                over_load_cost += (999999*(load > self.vehicle_capacity))

        total_cost = dist_cost + time_cost + over_load_cost
        # total_cost = dist_cost + time_cost
        # print(total_cost)
        fitness = 1 / total_cost
        return fitness

    def move_route_left(self):
        """
        remain two routes randomly
        :return:
        """
        depot_index = [ind for ind, val in enumerate(self.data) if val == self.depot]
        choose_pos = random.sample(depot_index[:-1], len(depot_index)-3)
        new_part_individual = list()
        for i in choose_pos:
            new_part_individual.extend(self.data[i:depot_index[depot_index.index(i)+1]])
        new_part_individual.append(self.depot)
        return new_part_individual


def nearest_neighbor(genes, distance_matrix):
    """
    sort the costumers by nearest neighbor
    """
    customer_num = len(genes)
    start_city = genes[0]
    solution_tour = [None for _ in range(customer_num)]
    solution_tour[0] = start_city
    visited = [start_city]
    for position in range(1, customer_num):
        last = solution_tour[position-1]
        min_distance = float('inf')
        for city in genes:
            if city not in visited:
                if distance_matrix[last.index][city.index] < min_distance:
                    min_distance = distance_matrix[last.index][city.index]
                    candidate_city = city
        solution_tour[position] = candidate_city
        visited.append(candidate_city)
    return solution_tour



def nearest_neighbor_chromosome(customers, depot, demand_list, distance_matrix, vehicle_capacity):
    """
    initialization randomly
    """
    customer_genes = customers
    random.shuffle(customer_genes)
    # based on customer distance and comment, randomly
    # customer_genes = nearest_neighbor(customer_genes, distance_matrix)
    # get the feasible solution
    chromosome = Chromosome(customer_genes, depot, demand_list, vehicle_capacity)
    return chromosome


def initial_population(customers, depot, demand_list, pop_size, distance_matrix, vehicle_capacity):
    return [nearest_neighbor_chromosome(customers, depot, demand_list, distance_matrix, vehicle_capacity) for _ in range(pop_size)]


def sort_population(population):
    """
    sort by solution distance
    """
    population.sort(key=lambda chromosome: chromosome.fitness, reverse=True)


def roulette_selection(population):
    """
    choose the individual by roulette
    """
    best_individual = population[0]
    bounds = sum([ind.fitness for ind in population])
    r = random.uniform(0, bounds)
    for individual in population:
        r -= individual.fitness
        if r <= 0:
            if individual == best_individual:
                individual_copy = deepcopy(individual)
                return individual_copy
            else:
                return individual


def crossover(p1, p2, depot, demand_list, vehicle_capacity):
    """
    cross the parent1 and parent2 sub-tour
    move the depot get the new routes
    """
    # choose the two sub-tour
    # print_data(p1.data)
    # print_data(p2.data)
    new_p1 = p1.move_route_left()
    new_p2 = p2.move_route_left()
    pos_1, pos_2 = len(new_p1) + 1, len(new_p2) + 1
    # two individuals crossover
    p1_part, p2_part = list(), list()
    for gene in p2.data:
        if gene not in new_p1:
            p1_part.append(gene)
    p1_part.sort(key=lambda gene: gene.start)
    for gene in p1.data:
        if gene not in new_p2:
            p2_part.append(gene)
    p2_part.sort(key=lambda gene: gene.start)
    new_p1.extend(p1_part)
    new_p1.append(depot)
    new_p2.extend(p2_part)
    new_p2.append(depot)
    # insert a depot to divide two routes and choose the best fitness
    key = lambda chromosome: chromosome.fitness
    possible = []
    while new_p1[pos_1] != depot:
        new_individual = new_p1.copy()
        new_individual.insert(pos_1, depot)
        new_individual = Chromosome(None, depot, demand_list, vehicle_capacity, new_individual)
        possible.append(new_individual)
        pos_1 += 1
    possible.sort(reverse=True, key=key)
    new_individual_p1 = possible[0]
    possible = []
    while new_p2[pos_2] != depot:
        new_individual = new_p2.copy()
        new_individual.insert(pos_2, depot)
        new_individual = Chromosome(None, depot, demand_list, vehicle_capacity, new_individual)
        possible.append(new_individual)
        pos_2 += 1
    possible.sort(reverse=True, key=key)
    new_individual_p2 = possible[0]
    # print_data(new_individual_p1.data)
    # print_data(new_individual_p2.data)
    # input('123')
    return new_individual_p1, new_individual_p2


def mutate_one(individual, depot, demand_list, vehicle_capacity):
    """
    two-opt, 10 different result to choose the best
    """
    mutate_gene_num = 10
    chromo_list = list()
    for i in range(mutate_gene_num):
        p1, p2 = random.sample(range(len(individual.data)), 2)
        new_individual = individual.data.copy()
        while new_individual[p1] == depot or new_individual[p2] == depot:
            p1, p2 = random.sample(range(len(individual.data)), 2)
        new_individual[p1], new_individual[p2] = new_individual[p2], new_individual[p1]
        chromo_list.append(Chromosome(None, depot, demand_list, vehicle_capacity, data=new_individual.copy()))
    chromo_list.sort(reverse=True, key=lambda chromosome: chromosome.fitness)
    return chromo_list[0]


def mutation(individual, depot, demand_list, vehicle_capacity):
    mutate_individual = mutate_one(individual, depot, demand_list, vehicle_capacity)
    return mutate_individual


def genetic_algorithm(population, next_gen_size, depot, demand_list, vehicle_capacity, crossover_pb=0.9, mutation_pb=0.1):
    """
    vrp by ga
    next_gen_size is even
    """
    next_population = list()
    next_population.extend(population[:2])  # remain the best individual in last generation
    # print(next_population[0].fitness)
    while len(next_population) != next_gen_size:
        # inserting elites
        p1 = roulette_selection(population)
        p2 = roulette_selection(population)
        # print(next_population[0].fitness)
        # crossover
        if random.random() < crossover_pb:
            offspring1, offspring2 = crossover(p1, p2, depot, demand_list, vehicle_capacity)
        else:
            offspring1, offspring2 = p1, p2
        # mutation
        if random.random() < mutation_pb:
            offspring1 = mutation(offspring1, depot, demand_list, vehicle_capacity)
            offspring2 = mutation(offspring2, depot, demand_list, vehicle_capacity)
        next_population.extend([offspring1, offspring2])
    sort_population(next_population)
    return next_population



    #     # crossover
    #     offspring_chromosome = crossover_sbx(p1, p2, depot, demand_list, vehicle_capacity)
    #     # mutation
    #     mutation(offspring_chromosome)
    #     next_population.append(offspring_chromosome)
    # # # draw_routes(crossover_chromosome[0].data)
    # # # copy the crossover chromosome to next population
    # # next_population = merge_chromosome(population, crossover_chromosome)
    # # # mutation
    # #   # under construction
    # sort_population(next_population)
    # return next_population




def draw_routes(routes):
    """
    print the routes
    :param routes:
    :return:
    """
    depot_position = list()
    all_routes = list()
    for index, node in enumerate(routes):
        if node.index == 0:
            depot_position.append(index)

    for i,j in zip(depot_position[:-1], depot_position[1:]):
        all_routes.append(routes[i:j+1])
    x_list = list()
    y_list = list()
    for route in all_routes:
        for n in route:
            x_list.append(n.x)
            y_list.append(n.y)
    plt.axis([10, 50, 40, 90])
    plt.scatter(x_list, y_list, c='r')
    plt.scatter(routes[0].x, routes[0].y, c='g')
    plt.plot(x_list, y_list)
    plt.show()


def print_data(data):
    show_list = list()
    for i in data:
        show_list.append(i.index)
    print(show_list)


