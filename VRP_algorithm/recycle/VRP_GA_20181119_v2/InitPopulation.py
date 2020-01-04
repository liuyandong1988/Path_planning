import Init_parameter
import random
from mdvrp_ga import Chromosome

def NearestNeighbor(start_city, city_number, init_tour, distance_matrix):
    solution_tour = [None for _ in range(city_number)]
    solution_tour[0] = start_city 
    start_city.visited = True
    for position in range(1, city_number):
        last = solution_tour[position-1]
        min_distance = float('inf')
        for city in init_tour:
            if not city.visited:
                if distance_matrix[last.id][city.id] < min_distance:
                    min_distance = distance_matrix[last.id][city.id]
                    candidate_city = city
        solution_tour[position] = candidate_city 
        candidate_city.visited = True
#         print candidate_city.id
#     aa = []
#     for node in solution_tour:
#         aa.append(node.id)
#     print aa 
    return solution_tour 


def minDistChromosome(customers, depots, distance_matrix, size):
    population = []
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
    new_genes = []
    for gene in genes:
        gene = NearestNeighbor(gene[0], len(gene), gene, distance_matrix)
        new_genes.append(gene)
#     aa = []
#     for node in new_genes[0]:
#         aa.append(node.id)
#     print aa
#     raw_input('prompt')
    for _ in range(size):
        add_genes = []
        for ind, gene in enumerate(new_genes):
            index1, index2 = random.sample(range(1,len(gene)), 2)
            index1, index2 = sorted([index1, index2])
            gene = gene[:index1] + gene[index2 :index1-1:-1] + gene[index2 +1:]   
            add_genes.append(gene)
        chromosome = Chromosome(add_genes, customers, depots)
        population.append(chromosome)
    return population

def initialPopulation(customers, depots, size, distance_matrix):
    return minDistChromosome(customers, depots, distance_matrix, size)  

def main():
    '''
    Nearest neighbor get the initialization result
    '''
    coordination, distance_matrix, Customers, Depots, depot_lists  = Init_parameter.initParam("A-n32-k5.vrp")
    pop_size = 20
    population = initialPopulation(Customers, Depots, pop_size, distance_matrix)
    cnt = 0
    for indi in population:
        aa = []
        cnt += 1
        for node in indi.genes[0]:
            aa.append(node.id)
        print ('Inidividual %s and genes:%s'%(cnt, aa))

if __name__ == '__main__':
    main()
