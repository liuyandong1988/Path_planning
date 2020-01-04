#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yandong
# Time  :2019/10/25 3:14
# initialization randomly !
# crossover, move the depot in the two route to optimize
# mutation, genes swap

import random, math
import matplotlib.pyplot as plt
import nearest_neighbor_initial as nn


class Chromosome(object):
    """Chromosome"""
    def __init__(self, genes, depot, distance_matrix, demand_list, vehicle_capacity, solution=None):

        self.genes = genes
        self.depot = depot
        self.distance_matrix = distance_matrix
        self.demand_list = demand_list
        self.vehicle_capacity = vehicle_capacity
        if not solution:
            self.feasible_solution = self._generate_chromosome(self.genes)
        else:
            self.feasible_solution = solution
        self.fitness = self.get_fitness()

    def _generate_chromosome(self, genes):
        """
        generate the feasible solution based on vehicle capacity
        """
        remain_nodes = genes[:]
        part_route = [self.depot]
        solution = list()
        nn_allow_nodes = remain_nodes[:]
        while remain_nodes:
            # find the nearest next node
            for j in nn_allow_nodes:
                next_node = j
            # check the time window
            ctw_mark, part_distance = check_tw(part_route, next_node, self.distance_matrix)
            if ctw_mark:
                # check the return depot time
                crdt_mark = check_return_depot_time(part_route, self.depot, self.distance_matrix)
                if crdt_mark:
                    # check the capacity constraint
                    cvc_mark = check_vehcile_capacity(part_route, self.vehicle_capacity)
                    if cvc_mark:
                        # satisfy all constraints and add the node to route
                        part_route.append(next_node)
                        last_node = next_node
                        remain_nodes.remove(next_node)
                        nn_allow_nodes = remain_nodes[:]
                    else:
                        # the next node cannot satisfy capacity constraint
                        nn_allow_nodes.remove(next_node)
                        if nn_allow_nodes == []:
                            # create a new route and reset the variables
                            solution, part_route, last_node, nn_allow_nodes = \
                                self.route_reset(solution, part_route, remain_nodes)
                else:
                    # cannot satisfy return depot constraint
                    nn_allow_nodes.remove(next_node)
                    if nn_allow_nodes == []:
                        # create a new route and reset the variables
                        solution, part_route, last_node, nn_allow_nodes = \
                            self.route_reset(solution, part_route, remain_nodes)
            else:
                # cannot satisfy time window
                nn_allow_nodes.remove(next_node)
                if nn_allow_nodes == []:
                    # create a new route and reset the variables
                    solution, part_route, last_node, nn_allow_nodes = \
                        self.route_reset(solution, part_route, remain_nodes)
        if len(part_route) > 1:
            # the remain route
            part_route.append(self.depot)
            solution.append(part_route)
        return solution

    def get_fitness(self):
        """
        calculate the fitness of solution
        :return:
        """
        fitness = 0
        dist_cost = 0
        # calculate distance
        for route in self.feasible_solution:
            for i, j in zip(route[:-1], route[1:]):
                dist_cost += self.distance_matrix[i.index][j.index]
        fitness = 1 / dist_cost
        return fitness

    def route_reset(self, solution, part_route, remain_nodes):
        """
        reset the variables
        """
        part_route.append(self.depot)
        solution.append(part_route)
        part_route = [self.depot]
        last_node = self.depot
        nn_allow_nodes = remain_nodes[:]
        return solution, part_route, last_node, nn_allow_nodes


def check_tw(part_route, next_node, distance_matrix):
    """
    Check the customer time window
    """
    total_travel_time = 0
    if len(part_route) != 1:
        for ind, node in enumerate(part_route):
            if ind == 0:
                continue
            else:
                last_node = part_route[ind-1]
                t_ij = distance_matrix[last_node.index][node.index]
                if ind == 1 and t_ij < node.start:
                    total_travel_time += (node.start + node.service)
                else:
                    total_travel_time += (t_ij + node.service)
    check_time_window = total_travel_time + distance_matrix[part_route[-1].index][next_node.index]
    if len(part_route) == 1 and check_time_window < next_node.start:
        check_time_window = next_node.start

    if next_node.start <= check_time_window <= next_node.end:
        total_travel_time = check_time_window
        total_travel_time += next_node.service
        return True, total_travel_time
    else:
        return False, None


def check_return_depot_time(total_route, depot, distance_matrix):
    """
    The return time must be in the depot end time
    """
    total_time = 0
    for ind, node in enumerate(total_route):
        if ind==0:
            continue
        else:
            last_node = total_route[ind-1]
            t_ij = distance_matrix[last_node.index][node.index]
            total_time += (t_ij+node.service)
    if total_time <= depot.end:
        return True
    else:
        return False


def check_vehcile_capacity(part_route, vehicle_capacity):
    """
    check the capacity constraint
    """
    total_demand = 0
    for customer in part_route:
        total_demand += customer.demand
    if total_demand <= vehicle_capacity:
        return True
    else:
        return False


def nearest_neighbor(customer_id, customer_distance, customers):
    """
    sort the costumers by nearest neighbor
    """
    near_customer = lambda c: customer_distance[c.index]
    customers.sort(key=near_customer)
    return customers


def initial_population(customers, depot, demand_list, distance_matrix, vehicle_capacity, pop_size, rand_ratio=0.8):
    """
    initialize the population, nearest neighbor and randomly
    """
    customer_num = len(customers)
    population = list()
    if customer_num < pop_size:
        pop_part1_num = customer_num
        pop_part2_num = pop_size-customer_num
    else:
        pop_part1_num = int(pop_size*rand_ratio)
        pop_part2_num = pop_size - pop_part1_num
    # nearest neighbor solution
    solution = nn.nearest_neighbor(customers, depot, distance_matrix, vehicle_capacity)
    genes = list()
    feasible_solution = list()
    for route in solution.values():
        feasible_solution.append(route)
        for node in route:
            if node != depot:
                genes.append(node)
    chromosome = Chromosome(genes, depot, distance_matrix, demand_list, vehicle_capacity, solution=feasible_solution)
    population.append(chromosome)
    # population part 1 nearest neighbor
    for i in range(1, pop_part1_num):
        # research neighbor
        new_customers = genes[i:] + genes[:i]
        # generate a new chromosome
        chromosome = Chromosome(new_customers, depot, distance_matrix, demand_list, vehicle_capacity)
        # print_solution(chromosome.feasible_solution, distance_matrix)
        # show_result(chromosome.feasible_solution, coordinates)
        population.append(chromosome)
    # population part2 randomly
    for i in range(pop_part2_num):
        random.shuffle(genes)
        chromosome = Chromosome(genes, depot, distance_matrix, demand_list, vehicle_capacity)
        # print_solution(chromosome.feasible_solution, distance_matrix)
        # show_result(chromosome.feasible_solution, coordinates)
        population.append(chromosome)
    return population


def sort_population(population):
    """
    sort by solution distance
    """
    population.sort(key=lambda chromosome: chromosome.fitness, reverse=True)


def ga_selection(population, tourney_size):
    """
    choose two individuals randomly, 90% select the min distance
    """
    tourney = random.sample(population, tourney_size)
    if random.random() < 0.9:
        return max(tourney, key=lambda chromosome: chromosome.fitness)
    return min(tourney, key=lambda chromosome: chromosome.fitness)


def ga_crossover(genes, tour, depot, distance_matrix, demand_list, vehicle_capacity):
    """
    put the customers in tour to insert the gene_1
    """
    for c in tour:
        if c in genes:
            genes.remove(c)
    stripped_solution = Chromosome(genes, depot, distance_matrix, demand_list, vehicle_capacity)
    for c in tour:
        stripped_cost = stripped_solution.fitness
        insertion_costs = []
        for i in range(len(genes)+1):
            genes.insert(i, c)
            insert_solution = Chromosome(genes, depot, distance_matrix, demand_list, vehicle_capacity)
            insertion_costs.append(insert_solution.fitness - stripped_cost)
            del genes[i]
        genes.insert(insertion_costs.index(max(insertion_costs)), c)
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


def recombination(p1, p2, crossover_possible, mutate, depot, distance_matrix, demand_list, vehicle_capacity, coordinates):
    """
    crossover and mutation
    """
    c1_genes = p1.genes[:]
    c2_genes = p2.genes[:]
    if random.random() <= crossover_possible:
        p1_tour = random.choice(p1.feasible_solution)[1:-1]
        p2_tour = random.choice(p2.feasible_solution)[1:-1]
        c2_genes = ga_crossover(c2_genes, p1_tour, depot, distance_matrix, demand_list, vehicle_capacity)
        c1_genes = ga_crossover(c1_genes, p2_tour, depot, distance_matrix, demand_list, vehicle_capacity)
    if mutate:
        mutation(c1_genes)
        mutation(c2_genes)
    aa = Chromosome(c1_genes, depot, distance_matrix, demand_list, vehicle_capacity)
    return Chromosome(c1_genes, depot, distance_matrix, demand_list, vehicle_capacity), \
           Chromosome(c2_genes, depot, distance_matrix, demand_list, vehicle_capacity)


def genetic_algorithm(population, next_gen_size, depot, demand_list, vehicle_capacity, distance_matrix, coordinates, crossover_possible=0.9, mutate_possible=0.1):
    """
    vrp by ga
    """
    new_pop = []
    selection_individual_number = 2
    mutate = False
    if random.random() <= mutate_possible:
        mutate = True  #  mutate operation
    # inherit the best 10 individuals
    for i in range(10):
        new_pop.append(population[i])
    # generate the offspring individual
    while len(new_pop) < next_gen_size:
        p1 = ga_selection(population, selection_individual_number)
        p2 = ga_selection(population, selection_individual_number)
        children = recombination(p1, p2, crossover_possible, mutate, depot, distance_matrix, demand_list, vehicle_capacity, coordinates)
        new_pop.extend(children)
    sort_population(new_pop)
    return new_pop

