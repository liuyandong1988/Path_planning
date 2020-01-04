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
    def __init__(self, g_delivery, g_pickup, depot, distance_matrix, vehicle_capacity):

        self.g_delivery = g_delivery
        self.g_pickup = g_pickup
        self.depot = depot
        self.distance_matrix = distance_matrix
        self.vehicle_capacity = vehicle_capacity
        self.feasible_solution = list()
        self._generate_chromosome()   # decode, get the routes
        self.fitness = self._get_fitness()

    def _generate_chromosome(self):
        """
        generate the feasible solution
        """
        self._decode_delivery_gene()
        self._decode_pickup_gene()

    def _decode_delivery_gene(self):
        """
        change the chromosome to routes based on the constraints
        """
        tmp_route = list()
        insert_mark = False
        tmp_route.append(self.depot)
        self.feasible_solution.append(tmp_route)
        first_delivery = self.g_delivery[:]
        while first_delivery:
            insert_node = first_delivery[0]
            # insert the tmp_route
            min_cost = float('inf')
            for index, route in enumerate(self.feasible_solution):
                if len(route) == 1:
                    route.append(insert_node)
                    route.append(self.depot)
                    self.feasible_solution[index] = route
                    first_delivery.remove(insert_node)
                    first_route_mark = True
                    continue
                else:
                    first_route_mark = False
                    for pos, node in enumerate(route):
                        if pos == 0:
                            continue
                        else:
                            # check time window, return window and capacity to decide insertion
                            if check_constrain(insert_node, pos, route, self.depot, self.distance_matrix, self.vehicle_capacity):
                                # insert the tmp route and record the pos
                                tmp_cost = cal_cost(insert_node, pos, route, self.distance_matrix.tolist())
                                if tmp_cost < min_cost:
                                    min_pos = pos
                                    insert_route_index = index
                                    insert_route = route
                                    min_cost = tmp_cost
                                    insert_mark = True
                                    break  # each route has only one feasible insertion

            if not first_route_mark:
                if insert_mark:
                    insert_mark = False
                    # choose the min pos to insert
                    insert_route.insert(min_pos, insert_node)
                    self.feasible_solution[insert_route_index] = insert_route
                    first_delivery.remove(insert_node)
                else:
                    # create new route
                    new_route = [self.depot, insert_node, self.depot]
                    self.feasible_solution.append(new_route)
                    first_delivery.remove(insert_node)

    def _decode_pickup_gene(self):
        """
        the pickup customers part
        """
        # pickup node insert the start position
        pickup_start_pos = list()
        insert_mark = False
        for r in self.feasible_solution:
            pickup_start_pos.append(len(r) - 1)
        # choose the insert position
        second_pickup = self.g_pickup[:]
        while second_pickup:
            insert_node = second_pickup[0]
            min_cost = float('inf')
            for index, route in enumerate(self.feasible_solution):
                for pos, node in enumerate(route):
                    if pos < pickup_start_pos[index]:
                        continue
                    else:
                        # if satisfy the constraints or not
                        if check_constrain(insert_node, pos, route, self.depot, self.distance_matrix, self.vehicle_capacity):
                            # insert the tmp route and record the pos
                            tmp_cost = cal_cost(insert_node, pos, route, self.distance_matrix.tolist())
                            if tmp_cost < min_cost:
                                min_pos = pos
                                insert_route_index = index
                                insert_route = route
                                min_cost = tmp_cost
                                insert_mark = True
                                break  # each route has only one feasible insertion
            if insert_mark:
                insert_mark = False
                # choose the min pos to insert
                insert_route.insert(min_pos, insert_node)
                self.feasible_solution[insert_route_index] = insert_route
                second_pickup.remove(insert_node)
            else:
                # create new route
                new_route = [self.depot, insert_node, self.depot]
                self.feasible_solution.append(new_route)
                second_pickup.remove(insert_node)
                pickup_start_pos.append(1)  # the pure pickup route

    def _get_fitness(self):
        """
        calculate the fitness of solution
        """
        dist_cost = 0
        distance_matrix = self.distance_matrix.tolist()
        # calculate distance
        for route in self.feasible_solution:
            for i, j in zip(route[:-1], route[1:]):
                dist_cost += distance_matrix[i.index][j.index]
        fitness = 1 / dist_cost
        return fitness


def check_constrain(node, pos, route, depot, distance_matrix, vehicle_capacity):
    if check_tw(node, pos, route, distance_matrix):
        # check the capacity
        if check_vehcile_capacity(node, route, vehicle_capacity):
            return True
    return False


def check_tw(insert_node, pos, part_route, distance_matrix):
    """
    Check the customer time window
    """
    total_travel_time = 0
    tmp_route = part_route[:pos]
    # before the insert node the time
    for ind, node in enumerate(tmp_route):
        if ind == 0:
            continue
        else:
            last_node = tmp_route[ind - 1]
            t_ij = distance_matrix[last_node.index][node.index]
            if ind == 1 and t_ij < node.start:
                total_travel_time += (node.start + node.service)
            else:
                total_travel_time += (t_ij + node.service)
    check_time_window = total_travel_time + distance_matrix[tmp_route[-1].index][insert_node.index]
    if len(tmp_route) == 1 and check_time_window < insert_node.start:
        check_time_window = insert_node.start
    if insert_node.start <= check_time_window <= insert_node.end:
        # check the after node
        next_node = part_route[pos]
        t_ij = distance_matrix[insert_node.index][next_node.index]
        check_time_window += (t_ij + insert_node.service)
        if pos == len(part_route):
            # next node is depot
            if check_time_window <= next_node.end:
                return True
        else:
            if next_node.start <= check_time_window <= next_node.end:
                return True
    # violate the time window
    return False


def check_vehcile_capacity(node, route, vehicle_capacity):
    """
    check the capacity constraint
    """
    total_demand = 0
    delivery_demand, pickup_demand = 0, 0
    for customer in route:
        if customer.pd_mark == 0:
            # pickup
            pickup_demand += customer.demand
        else:
            # delivery
            delivery_demand += customer.demand
    if node.pd_mark == 0:
        pickup_demand += customer.demand
        total_demand = pickup_demand
    else:
        delivery_demand += customer.demand
        total_demand = delivery_demand
    if total_demand <= vehicle_capacity:
        return True
    else:
        return False


def cal_cost(insert_node, pos, route, distance_matrix, alphy=1, beta_1=1, beta_2=0):
    """
    the cost of distance and service time
    """
    before_node, after_node = route[pos - 1], route[pos]
    i, u, j = before_node.index, insert_node.index, after_node.index
    cost_distance = distance_matrix[i][u] + distance_matrix[u][j] - alphy * distance_matrix[j][i]
    cost_time = distance_matrix[i][u] + insert_node.service + distance_matrix[u][j] - distance_matrix[j][i]
    total_cost = beta_1 * cost_distance + beta_2 * cost_time
    return total_cost


def initial_population(delivery_c, pickup_c, depot, distance_matrix, vehicle_capacity, pop_size):
    """
    initialize the population, min insert
    """
    population = list()
    for i in range(pop_size):
        d_genes, p_genes = delivery_c[:], pickup_c[:]
        random.shuffle(d_genes)
        random.shuffle(p_genes)
        chromosome = Chromosome(d_genes, p_genes, depot, distance_matrix, vehicle_capacity)
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


def ga_crossover_distance(f_genes, m_genes, distance_matrix):
    """
    compare the two chromosome and chose the distance better gene
    """
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


def ga_crossover_time(f_genes, m_genes):
    """
    compare the two chromosome and chose the time better gene
    """
    # choose the earliest time gene
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
                      crossover_possible=0.9, mutate_possible=0.1):
    """
    vrp by ga
    """
    new_pop = []
    # inherit the best 10 individuals
    for i in range(2):
        new_pop.append(population[i])
    # generate the offspring individual
    while len(new_pop) < pop_size:
        # selection
        p1 = ga_selection(population, tourney_size=3)
        p2 = ga_selection(population, tourney_size=3)
        # crossover by distance or time start
        p1_delivery_genes, p1_pickup_genes = p1.g_delivery, p1.g_pickup
        p2_delivery_genes, p2_pickup_genes = p2.g_delivery, p2.g_pickup
        # pickup and delivery genes
        d_distance_genes = ga_crossover_distance(p1_delivery_genes, p2_delivery_genes, distance_matrix.tolist())
        p_distance_genes = ga_crossover_distance(p1_pickup_genes, p2_pickup_genes, distance_matrix.tolist())
        d_time_genes = ga_crossover_time(p1_delivery_genes, p2_delivery_genes)
        p_time_genes = ga_crossover_time(p1_pickup_genes, p2_pickup_genes)
        if random.random() < mutate_possible:
            mutation(d_distance_genes)
            mutation(p_distance_genes)
            mutation(d_time_genes)
            mutation(p_time_genes)
        offspring_1 = Chromosome(d_distance_genes, p_distance_genes, depot, distance_matrix, vehicle_capacity)
        offspring_2 = Chromosome(d_time_genes, p_time_genes, depot, distance_matrix, vehicle_capacity)
        new_pop.extend([offspring_1, offspring_2])
    sort_population(new_pop)
    return new_pop


def print_route(solution):
    for i,route in enumerate(solution):
        route_list = list()
        for n in route:
            route_list.append(n.index)
        print('Route %s %s'%(i, route_list))

