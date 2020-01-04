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


def initial_population(customers, depot, demand_list, distance_matrix, vehicle_capacity, pop_size, rand_ratio=0.5):
    """
    initialize the population, nearest neighbor and randomly
    """
    customer_num = len(customers)
    population = list()
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
    chromosome = Chromosome(genes[:], depot, distance_matrix, demand_list, vehicle_capacity, solution=feasible_solution)
    population.append(chromosome)
    # population part 1 nearest neighbor
    for i in range(1, pop_part1_num, 3):
        # research neighbor
        new_customers = genes[i:] + genes[:i]
        # generate a new chromosome
        chromosome = Chromosome(new_customers[:], depot, distance_matrix, demand_list, vehicle_capacity)
        # print_solution(chromosome.feasible_solution, distance_matrix)
        # show_result(chromosome.feasible_solution, coordinates)
        population.append(chromosome)
    # population part2 randomly
    for i in range(pop_part2_num):
        random.shuffle(genes)
        chromosome = Chromosome(genes[:], depot, distance_matrix, demand_list, vehicle_capacity)
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


def ga_crossover_distance(f_chromosome, m_chromosome, distance_matrix):
    """
    compare the two chromosome and chose the distance better gene
    """
    f_genes, m_genes = f_chromosome.genes[:], m_chromosome.genes[:]
    first_gene_pos = m_genes.index(f_genes[0])
    m_genes[0], m_genes[first_gene_pos] = m_genes[first_gene_pos], m_genes[0]
    # distance crossover
    new_genes = list()
    new_genes.append(m_genes[0])
    for pos in range(1, len(f_genes)):
        if distance_matrix[new_genes[pos-1].index][f_genes[pos].index] <= \
                distance_matrix[new_genes[pos-1].index][m_genes[pos].index]:
            min_gene = f_genes[pos]
            swap_pos = m_genes.index(min_gene)
            m_genes[pos], m_genes[swap_pos] = m_genes[swap_pos], m_genes[pos]
        else:
            min_gene = m_genes[pos]
            swap_pos = f_genes.index(min_gene)
            f_genes[pos], f_genes[swap_pos] = f_genes[swap_pos], f_genes[pos]
        new_genes.append(min_gene)
    return new_genes


def ga_crossover_time(f_chromosome, m_chromosome):
    """
    compare the two chromosome and chose the time better gene
    """
    # choose the earliest time gene
    f_genes, m_genes = f_chromosome.genes[:], m_chromosome.genes[:]
    min_distance_genes = f_genes[:]
    min_distance_genes.sort(key=lambda gene:gene.start)
    new_genes = list()
    time_min_gene = min_distance_genes[0]
    new_genes.append(time_min_gene)
    # swap the fist gene for father and mother
    f_swap_pos = f_genes.index(time_min_gene)
    f_genes[0], f_genes[f_swap_pos] = f_genes[f_swap_pos], f_genes[0]
    m_swap_pos = m_genes.index(time_min_gene)
    m_genes[0], m_genes[m_swap_pos] = m_genes[m_swap_pos], m_genes[0]
    for pos in range(1, len(f_genes)):
        if f_genes[pos].start <= m_genes[pos].start:
            min_gene = f_genes[pos]
            swap_pos = m_genes.index(min_gene)
            m_genes[pos], m_genes[swap_pos] = m_genes[swap_pos], m_genes[pos]
        else:
            min_gene = m_genes[pos]
            swap_pos = f_genes.index(min_gene)
            f_genes[pos], f_genes[swap_pos] = f_genes[swap_pos], f_genes[pos]
        new_genes.append(min_gene)
    return new_genes


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


def genetic_algorithm(population, depot, demand_list, vehicle_capacity, distance_matrix, coordinates, pop_size,
                      crossover_possible=0.9, mutate_possible=0.3):
    """
    vrp by ga
    """
    new_pop = []
    # inherit the best 10 individuals
    for i in range(10):
        new_pop.append(population[i])
    # generate the offspring individual
    while len(new_pop) < pop_size:
        # selection
        p1 = ga_selection(population, tourney_size=3)
        p2 = ga_selection(population, tourney_size=3)
        # crossover by distance or time start
        cross_distance_genes = ga_crossover_distance(p1, p2, distance_matrix.tolist())
        cross_time_genes = ga_crossover_time(p1, p2)
        if random.random() < mutate_possible:
            mutation(cross_distance_genes)
            mutation(cross_time_genes)
        offspring_1 = Chromosome(cross_distance_genes, depot, distance_matrix, demand_list, vehicle_capacity)
        offspring_2 = Chromosome(cross_time_genes, depot, distance_matrix, demand_list, vehicle_capacity)
        new_pop.extend([offspring_1, offspring_2])
    sort_population(new_pop)
    return new_pop

def print_genes(genes):
    aa = list()
    for i in genes:
        aa.append(i.index)
    print(aa)

