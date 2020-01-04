import random, math, point, os
import localsearch as ls
 
class Chromosome(object):
    """docstring for Chromosome"""
    def __init__(self, genes, customers, depots):
        super(Chromosome, self).__init__()
        self.genes = genes
        self.customers = customers
        self.depots = depots
        self.solution = None

    def get_solution(self):
        if self.solution == None:
            self.solution = MDVRPSolution(self)
        return self.solution

    def get_copy(self):
        genes_copy = []
        for gene in self.genes:
            genes_copy.append(gene[:])
        return Chromosome(genes_copy, self.customers, self.depots)

class MDVRPSolution(object):
    """Docstring decode the genes to tours"""
    def __init__(self, chromosome):
        super(MDVRPSolution, self).__init__()
        self.tours = [[] for i in range(len(chromosome.genes))]
        self.customers = chromosome.customers
        self.depots = chromosome.depots 
        for i in range(len(chromosome.genes)):
            self.tours[i] = self._schedule_tours(chromosome.genes[i], self.depots[i])
        self.total_distance = 0
#         print self.tours
#         raw_input('prompt') 
        for depot in self.tours:
            for tour in depot:
                self.total_distance += self._tour_dist(tour)

    def reschedule_depot(self, depot_cluster, i):
#         print depot_cluster
        for tour in self.tours[i]:
            self.total_distance -= self._tour_dist(tour)
        self.tours[i] = self._schedule_tours(depot_cluster, self.depots[i])
        for tour in self.tours[i]:
            self.total_distance += self._tour_dist(tour)

    def _schedule_tours(self, depot_cluster, d):
        routes = []
        length = 0
        load = 0
        tour = [d]
        for c in depot_cluster:
            if c.duration == None:
                c.duration = 0
            total_duration = length + c.distance(tour[-1]) + c.duration + d.distance(c)
            if load + c.demand <= d.max_load and d.duration_check(total_duration):
                tour.append(c)
                length += c.distance(tour[-1]) + c.duration
                load += c.demand
            else:
                tour.append(d)
                routes.append(tour)
                length = 0
                load = 0
                tour = [d]
                total_duration = length + c.distance(tour[-1]) + c.duration + d.distance(c)
                assert load + c.demand <= d.max_load and d.duration_check(total_duration)
                tour.append(c)
                length += c.distance(tour[-1]) + c.duration
                load += c.demand
        tour.append(d)
#         print tour
        routes.append(tour)
        #build second alternative
        routes2 = [route for route in routes]
        for i in range(len(routes2)):
            routes2[i] = routes2[i][1:-1]
        for i in range(1, len(routes2)):
            routes2[i] = [routes2[i-1][-1]] + routes2[i]
            routes2[i-1] = routes2[i-1][:-1]
        for i in range(len(routes2)):
            routes2[i] = [d] + routes2[i] + [d]
        valid = True
        for route in routes2:
            if not (d.duration_check(self._tour_dist(route)) and self._tour_load(route) <= d.max_load):
                valid = False
                break
        if valid and self._routes_dist(routes) >= self._routes_dist(routes2):
            return routes2
        return routes

    def _tour_dist(self, tour):
        distance = 0
        for i in range(1, len(tour)):
            distance += tour[i].distance(tour[i-1])
        return distance

    def _routes_dist(self, tours):
        distance = 0
        for tour in tours:
            distance += self._tour_dist(tour)
        return(distance)

    def _tour_load(self, tour):
        load = 0
        for customer in tour[1:-1]:
            load += customer.demand
        return load

    def write_to_file(self):
        with open('p01_s', 'w') as f:
            f.write("{:.2f}".format(self.total_distance))
            f.write('\n')
            for i in range(len(self.tours)):
                depot = self.tours[i]
                for j in range(len(depot)):
                    tour = depot[j]
                    f.write(str(i+1)+' ')
                    f.write(str(j+1)+' ')
                    f.write("{:.2f}".format(self._tour_dist(tour))+' ')
                    f.write('0 ')
                    for pnt in tour[1:-1]:
                        f.write(str(pnt.id)+' ')
                    f.write('0')
                    f.write('\n')

def minDistRandomChromosome(customers, depots):
    genes = [[] for _ in range(len(depots))]
    for customer in customers:
        min_dist_d = 0
        min_dist = customer.distance(depots[0])
        for depot in depots[1:]:
            curr_dist = customer.distance(depot)
            if curr_dist < min_dist:
                min_dist_d = depot.id
                min_dist = curr_dist
        genes[min_dist_d].append(customer)
    for gene in genes:
        random.shuffle(gene)
    chromosome = Chromosome(genes, customers, depots)
    return chromosome

def initialPopulation(customers, depots, size):
    return [minDistRandomChromosome(customers, depots) for _ in range(size)]

def tournamentSelect(population, tourney_size):
    tourney = random.sample(population, tourney_size)
    if random.random() < 0.9:
        return min(tourney, key=lambda chromosome: chromosome.get_solution().total_distance)
    return max(tourney, key=lambda chromosome: chromosome.get_solution().total_distance)

def bestCostCrossover(genes, depot, tour, C, D):
    for d in genes:
        for c in tour:
            if c in d:
                d.remove(c)
    stripped_solution = Chromosome(genes, C, D).get_solution()
    for c in tour:
        stripped_cost = stripped_solution.total_distance
        insertion_costs = []
#         print len(genes[depot]), genes[depot]
#         raw_input('prompt')
        for i in range(len(genes[depot])+1):
            genes[depot].insert(i, c)
#             print len(genes[depot]), genes[depot]
            stripped_solution.reschedule_depot(genes[depot], depot)
            insertion_costs.append(stripped_solution.total_distance - stripped_cost)
            del genes[depot][i]
        genes[depot].insert(insertion_costs.index(min(insertion_costs)), c)
        stripped_solution.reschedule_depot(genes[depot], depot)
    return genes

def reversal_mutation(gene):
    cutpoints = random.sample(range(len(gene)), 2)
    cutpoints.sort()
    gene[cutpoints[0]:cutpoints[1]] = gene[cutpoints[0]:cutpoints[1]][::-1]

def swap_mutation(gene):
    swap_points = random.sample(range(len(gene)), 2)
    gene[swap_points[0]], gene[swap_points[1]] = gene[swap_points[1]], gene[swap_points[0]]

def mutation(genes):
    gene = random.choice(genes)
    if random.random() <= 0.5:
        reversal_mutation(gene)
    else:
        swap_mutation(gene)

def recombination(p1, p2, mutate):
    '''
    crossover and mutation
    '''
    crossover_possible = 0.8
    c1_genes = p1.get_copy().genes
    c2_genes = p2.get_copy().genes
#     print c1_genes 
#     raw_input('prompt')
    if random.random() <= crossover_possible:
        depot = random.randrange(0, len(p1.genes))
        p1_tour = random.choice(p1.get_solution().tours[depot])[1:-1]
        p2_tour = random.choice(p2.get_solution().tours[depot])[1:-1]
        c2_genes = bestCostCrossover(c2_genes, depot, p1_tour, p1.customers, p1.depots)
        c1_genes = bestCostCrossover(c1_genes, depot, p2_tour, p1.customers, p1.depots)
    if mutate:
        mutation(c1_genes)
        mutation(c2_genes)
    return Chromosome(c1_genes, p1.customers, p1.depots), Chromosome(c2_genes, p1.customers, p1.depots)


def sortPop(population):
    population.sort(key = lambda chromosome: chromosome.get_solution().total_distance)


def geneticAlgorithm(population, next_gen_size, coordination, distance_matrix, customers, depots):
    '''
    GA algorithm gets result
    '''
    new_pop = []
    mutate_possible = 0.2
    selection_individual_number = 4 
    best_individual_num = 3
    #inserting three elites
    for i in range(best_individual_num):
        new_pop.append(population[i])
    #filling in with children
    mutate = False
    if random.random() <= mutate_possible:
        mutate = True
    while len(new_pop) < next_gen_size:
        p1 = tournamentSelect(population, selection_individual_number)
        p2 = tournamentSelect(population, selection_individual_number)
        children = recombination(p1, p2, mutate)
        for child in children:
            child = ls.routeToOptTwo(child, coordination, distance_matrix, customers, depots)
            new_pop.append(child)
    sortPop(new_pop)
    return new_pop


