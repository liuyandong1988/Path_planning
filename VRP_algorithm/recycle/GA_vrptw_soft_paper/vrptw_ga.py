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
    def __init__(self, genes, depot, demand_list, vehicle_capacity, data=None, waiting_penalty=0, delay_penalty=1000):

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
        self.fitness = self.get_fitness(self.data)

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

    def get_fitness(self, data):
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
        while i < len(data):
            cal_distance = lambda x1, y1, x2, y2: math.sqrt(math.pow(x1-x2, 2)+math.pow(y1-y2, 2))
            part_distance.append(cal_distance(data[i].x, data[i].y, data[i-1].x, data[i-1].y))
            i += 1
        dist_cost = sum(part_distance)

        # time cost: travel_time + penalty_cost + service_time
        time_spend = 0
        for ind, pos in enumerate(data):
            if pos.index == 0:
                time_spend = 0
            if ind != 0:
                # travel time
                time_spend += cal_distance(pos.x, pos.y, data[ind-1].x, data[ind-1].y)
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
        for index, gene in enumerate(data):
            if index == 0:
                continue
            elif gene.index == 0:
                load = 0
            else:
                load += self.demand_list[gene.index]
                over_load_cost += (999999*(load > self.vehicle_capacity))

        total_cost = dist_cost + time_cost + over_load_cost
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


def insert_node_fitness(parent, node):
    """
    insert the node to the best position
    """
    best_fitness = -float('inf')
    best_position = None
    for pos in range(1, len(parent.data)):
        data = parent.data[:]
        data.insert(pos, node)
        current_fitness = parent.get_fitness(data)
        if current_fitness > best_fitness:
            best_position = pos
            best_fitness = current_fitness
    parent.data.insert(best_position, node)
    # print_data(parent.data)


def sbx_routes(p1, cross_route1, cross_route2, vehicle_capacity):
    break_link1 = random.randint(1, len(cross_route1)-1)
    break_link2 = random.randint(1, len(cross_route2) - 1)
    # new route
    new_route = cross_route1[:break_link1]
    for node in cross_route2[break_link2:]:
        if node in new_route:
            continue
        else:
            new_route.append(node)
    new_route.append(new_route[0])
    remain_nodes = [node for node in cross_route1 if node not in new_route]
    remove_nodes = list()
    # repair1: remove the repeat node in p1 routes
    for node in p1.data:
        if node.index != 0 and node in new_route:
            remove_nodes.append(node)
    for node in remove_nodes:
        p1.data.remove(node)
    p1.data.extend(new_route[1:])
    # repair2: insert the remain node
    for node in remain_nodes:
        insert_node_fitness(p1, node)

def data_to_routes(data):
    # find the routes from parent 1
    route_depot_index = [i for i, x in enumerate(data) if x.index == 0]
    routes = list()
    for i, j in zip(route_depot_index[:-1], route_depot_index[1:]):
        new_route = data[i:j + 1]
        routes.append(new_route)
    return routes

def crossover_sbx(p1, p2, depot, demand_list, vehicle_capacity):
    """
    crossover by sequence base
    """
    # find the routes from parent 1
    p1_routes = data_to_routes(p1.data)
    # find the routes from parent 2
    p2_routes = data_to_routes(p2.data)
    # choose the exchange the two routes
    cross_route1 = random.choice(p1_routes)
    cross_route2 = random.choice(p2_routes)
    index_next = 0
    while cross_route1 == cross_route2:
        cross_route2 = p2_routes[index_next]
        index_next += 1
    # generate the offspring by crossover
    new_data = []
    for route in p1_routes:
        if route != cross_route1:
            new_data.extend(route[:-1])
    new_data.append(depot)
    p1.data = new_data  # remove the cross route
    sbx_routes(p1, cross_route1, cross_route2, vehicle_capacity)
    return p1




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


def mutation(parent, mut_pob=0.5):
    if random.random() < mut_pob:
        routes = data_to_routes(parent.data)
        # choose the shortest route
        mutation_route = [n for n in routes if len(n) == min([len(r) for r in routes])][0]
        # print_data(mutation_route)
        # print_data(parent.data)
        for node in mutation_route[1:-1]:
            parent.data.remove(node)
            # print_data(parent.data)
            insert_node_fitness(parent, node)



    # return chromosomes


def genetic_algorithm(population, next_gen_size, depot, demand_list, vehicle_capacity):
    """
    vrp by ga
    """
    next_population = list()
    next_population.extend(population[:10])
    while len(next_population) != next_gen_size:
        # inserting elites
        p1 = roulette_selection(population)
        p2 = roulette_selection(population)
        # crossover
        offspring_chromosome = crossover_sbx(p1, p2, depot, demand_list, vehicle_capacity)
        # mutation
        mutation(offspring_chromosome)
        next_population.append(offspring_chromosome)
    # # draw_routes(crossover_chromosome[0].data)
    # # copy the crossover chromosome to next population
    # next_population = merge_chromosome(population, crossover_chromosome)
    # # mutation
    #   # under construction
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

def print_routes(routes):
    for r in routes:
        print_data(r)


