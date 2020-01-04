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
    def __init__(self, genes, depot, demand_list, vehicle_capacity, data=None):

        self.genes = genes
        self.depot = depot
        self.demand_list = demand_list
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
        over_load_cost = 0
        part_distance = list()

        # calculate distance
        i = 1
        while i < len(self.data):
            cal_distance = lambda x1, y1, x2, y2: math.sqrt(math.pow(x1-x2, 2)+math.pow(y1-y2, 2))
            part_distance.append(cal_distance(self.data[i].x, self.data[i].y, self.data[i-1].x, self.data[i-1].y))
            i += 1
        dist_cost = sum(part_distance)

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

        total_cost = dist_cost + over_load_cost
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
    customer_genes = nearest_neighbor(customer_genes, distance_matrix)
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


def ga_selection(population, pop_size):
    """
    choose 1/3 best individual
    """
    num = int(pop_size / 6) * 2
    return population[:num]


def ga_crossover(chromosomes, depot, demand_list, vehicle_capacity):
    """
    move the depot get the new routes
    """
    crossover_chromosome = list()
    for i in range(0, len(chromosomes), 2):
        individual_1, individual_2 = chromosomes[i], chromosomes[i + 1]  # two crossover individuals
        new_individual_1 = individual_1.move_route_left()
        new_individual_2 = individual_2.move_route_left()
        ind_pos_1, ind_pos_2 = len(new_individual_1) + 1, len(new_individual_2) + 1
        # two individuals crossover
        for gene in individual_2.data:
            if gene not in new_individual_1:
                new_individual_1.append(gene)
        for gene in individual_1.data:
            if gene not in new_individual_2:
                new_individual_2.append(gene)
        new_individual_1.append(depot)
        new_individual_2.append(depot)
        # insert a depot to divide two routes and choose the best fitness
        key = lambda chromosome: chromosome.fitness
        possible = []
        while new_individual_1[ind_pos_1] != depot:
            new_individual = new_individual_1.copy()
            new_individual.insert(ind_pos_1, depot)
            new_individual = Chromosome(None, depot, demand_list, vehicle_capacity, new_individual)
            possible.append(new_individual)
            ind_pos_1 += 1
        possible.sort(reverse=True, key=key)
        crossover_chromosome.append(possible[0])
        possible = []
        while new_individual_2[ind_pos_2] != depot:
            new_individual = new_individual_2.copy()
            new_individual.insert(ind_pos_2, depot)
            new_individual = Chromosome(None, depot, demand_list, vehicle_capacity, new_individual)
            possible.append(new_individual)
            ind_pos_2 += 1
        possible.sort(reverse=True, key=key)
        crossover_chromosome.append(possible[0])
    return crossover_chromosome


def merge_chromosome(last_pop, cross_pop):
    """
    cross_pop instead of the worse last_pop
    """
    pop_size = len(last_pop)
    pos = pop_size - 1
    for chromo in cross_pop:
        last_pop[pos] = chromo
        pos -= 1
    return last_pop



def mutate_one(individual, depot, demand_list, vehicle_capacity):
    mutate_gene_num = 10
    new_individual = list()
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



def mutation(chromosomes, depot, demand_list, vehicle_capacity, mut_pob = 0.2):
    for index, individual in enumerate(chromosomes):
        # remain the best 30
        if index < 30:
            continue
        if random.random() < mut_pob:
            chromosomes[index] = mutate_one(individual, depot, demand_list, vehicle_capacity)
    return chromosomes


def genetic_algorithm(population, next_gen_size, depot, demand_list, vehicle_capacity):
    """
    vrp by ga
    """
    # inserting elites
    selection_chromosome = ga_selection(deepcopy(population), next_gen_size)
    # crossover
    crossover_chromosome = ga_crossover(selection_chromosome, depot, demand_list, vehicle_capacity)
    # copy the crossover chromosome to next population
    next_population = merge_chromosome(population, crossover_chromosome)
    # mutation
    next_population = mutation(next_population, depot, demand_list, vehicle_capacity)  # under construction
    sort_population(next_population)
    return next_population




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

    plt.plot(x_list, y_list)
    plt.show()


def print_data(data):
    show_list = list()
    for i in data:
        show_list.append(i.index)
    print(show_list)


