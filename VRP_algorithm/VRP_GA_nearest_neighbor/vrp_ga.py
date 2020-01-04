#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/25 3:14
# initialization randomly !
# crossover, genes and a feasible route exchange.
# mutation, genes swap or reverse

import random


def print_route(tours):
    for i in tours:
        aa = list()
        for n in i:
            aa.append(n.id)
        print(aa)


class Chromosome(object):
    """docstring for Chromosome"""
    def __init__(self, genes, depot):
        super(Chromosome, self).__init__()
        self.genes = genes
        self.depot = depot
        self.solution = None

    def get_solution(self):
        if self.solution == None:
            self.solution = vrp_solution(self)
        return self.solution

    def get_copy(self):
        genes_copy = self.genes[:]
        return Chromosome(genes_copy, self.depot)

class vrp_solution(object):
    """Docstring decode the genes to tours"""
    def __init__(self, chromosome):
        super(vrp_solution, self).__init__()
        self.depot = chromosome.depot
        self.tours = self._schedule_tours(chromosome.genes, self.depot)
        self.total_distance = self._routes_dist(self.tours)

    def _schedule_tours(self, customers, depot):
        routes = []
        length = 0
        load = 0
        tour = [depot]
        for c in customers:
            # pass length - this part - service time - return to depot
            total_duration = length + c.distance(tour[-1]) + c.service_time + depot.distance(c)
            if load + c.demand <= depot.vehicle_max_load and depot.duration_check(total_duration):
                tour.append(c)
                length += c.distance(tour[-1]) + c.service_time
                load += c.demand
            else:
                # the another new route
                tour.append(depot)
                routes.append(tour)
                length = 0
                load = 0
                tour = [depot]
                total_duration = length + c.distance(tour[-1]) + c.service_time + depot.distance(c)
                assert load + c.demand <= depot.vehicle_max_load and depot.duration_check(total_duration)
                tour.append(c)
                length += c.distance(tour[-1]) + c.service_time
                load += c.demand
        tour.append(depot)
        routes.append(tour)
        # build second alternative
        routes2 = [route for route in routes]
        for i in range(len(routes2)):
            routes2[i] = routes2[i][1:-1]
        for i in range(1, len(routes2)):
            routes2[i] = [routes2[i - 1][-1]] + routes2[i]
            routes2[i - 1] = routes2[i - 1][:-1]
        for i in range(len(routes2)):
            routes2[i] = [depot] + routes2[i] + [depot]
        valid = True
        for route in routes2:
            if not ((depot.duration_check(self._tour_dist(route)) and
                     self._tour_load(route) <= depot.vehicle_max_load)):
                valid = False
                break
        if valid and self._routes_dist(routes) >= self._routes_dist(routes2):
            return routes2
        return routes

    def _tour_dist(self, tour):
        distance = 0
        for i in range(1, len(tour)):
            distance += tour[i].distance(tour[i-1])
            if tour[i].id != 0:
                distance += tour[i].service_time  # except depot
        return distance

    def _tour_load(self, tour):
        load = 0
        for customer in tour[1:-1]:
            load += customer.demand
        return load

    def _routes_dist(self, tours):
        distance = 0
        for tour in tours:
            distance += self._tour_dist(tour)
        return distance


def nearest_neighbor(genes, distance_matrix):
    """
    sort the costumers by nearest neighbor
    """
    customer_num = len(genes)
    start_city = genes[0]
    solution_tour = [None for _ in range(customer_num)]
    solution_tour[0] = start_city
    start_city.visited = True
    for position in range(1, customer_num):
        last = solution_tour[position-1]
        min_distance = float('inf')
        for city in genes:
            if not city.visited:
                if distance_matrix[last.id][city.id] < min_distance:
                    min_distance = distance_matrix[last.id][city.id]
                    candidate_city = city
        solution_tour[position] = candidate_city
        candidate_city.visited = True
    for customer in genes:
        customer.visited = False  # reset
    return solution_tour



def nearest_neighbor_chromosome(customers, depot, distance_matrix):
    """
    initialization randomly
    """
    customer_genes = customers
    random.shuffle(customer_genes)
    customer_genes = nearest_neighbor(customer_genes, distance_matrix)
    chromosome = Chromosome(customer_genes, depot)
    return chromosome


def initial_population(customers, depot, pop_size, distance_matrix):
    return [nearest_neighbor_chromosome(customers, depot, distance_matrix) for _ in range(pop_size)]


def sort_population(population):
    """
    sort by solution distance
    """
    population.sort(key=lambda chromosome: chromosome.get_solution().total_distance)


def genetic_algorithm(population, next_gen_size, depot, inherit_num=5, crossover_possible=0.8, mutate_possible=0.2):
    """
    vrp by ga
    """
    new_pop = []
    selection_individual_number = 2
    # inserting elites
    for i in range(inherit_num):
        new_pop.append(population[i])
    # filling in with children
    mutate = False
    if random.random() <= mutate_possible:
        mutate = True  #  mutate operation
    while len(new_pop) < next_gen_size:
        print(len(new_pop))
        p1 = ga_selection(population, selection_individual_number)
        p2 = ga_selection(population, selection_individual_number)
        children = recombination(p1, p2, crossover_possible, mutate, depot)
        new_pop.extend(children)
    sort_population(new_pop)
    return new_pop


def ga_selection(population, tourney_size):
    """
    choose two individuals randomly, 90% select the min distance
    """
    tourney = random.sample(population, tourney_size)
    if random.random() < 0.9:
        return min(tourney, key=lambda chromosome: chromosome.get_solution().total_distance)
    return max(tourney, key=lambda chromosome: chromosome.get_solution().total_distance)


def recombination(p1, p2, crossover_possible, mutate, depot):
    """
    crossover and mutation
    """
    c1_genes = p1.get_copy().genes
    c2_genes = p2.get_copy().genes
    if random.random() <= crossover_possible:
        p1_tour = random.choice(p1.get_solution().tours)[1:-1]
        p2_tour = random.choice(p2.get_solution().tours)[1:-1]
        c2_genes = ga_crossover(c2_genes, p1_tour, depot)
        c1_genes = ga_crossover(c1_genes, p2_tour, depot)
    if mutate:
        mutation(c1_genes)
        mutation(c2_genes)
    return Chromosome(c1_genes, depot), Chromosome(c2_genes, depot)


def ga_crossover(genes, tour, depot):
    """
    put the customers in tour to insert the gene_1
    """
    for c in tour:
        if c in genes:
            genes.remove(c)
    stripped_solution = Chromosome(genes, depot).get_solution()
    for c in tour:
        stripped_cost = stripped_solution.total_distance
        insertion_costs = []
        for i in range(len(genes)+1):
            genes.insert(i, c)
            insert_solution = Chromosome(genes, depot).get_solution()
            insertion_costs.append(insert_solution.total_distance - stripped_cost)
            del genes[i]
        genes.insert(insertion_costs.index(min(insertion_costs)), c)
    return genes

def mutation(genes):
    # two mutation: swap, reversal
    if random.random() <= 0.5:
        reversal_mutation(genes)
    else:
        swap_mutation(genes)


def reversal_mutation(genes):
    cutpoints = random.sample(range(len(genes)), 2)
    cutpoints.sort()
    genes[cutpoints[0]:cutpoints[1]] = genes[cutpoints[0]:cutpoints[1]][::-1]

def swap_mutation(genes):
    swap_points = random.sample(range(len(genes)), 2)
    genes[swap_points[0]], genes[swap_points[1]] = genes[swap_points[1]], genes[swap_points[0]]