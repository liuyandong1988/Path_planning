__author__ = 'Yuzhe'
import numpy as np
import math
import support


'''sort function'''
def getKey(item):
    return item[1]

'''nearest neighbor heuristic'''
def nearest_neighboor(DistancePheromoneMatrix_tmp, RandomVector, nn):

    # define the greedy level of bees
    nn = np.random.choice([1,2,3], 1, p=[0.2,0.3,0.5])[0]
    prob_list = np.empty( (nn), float )
    nearest_neighbor = np.empty((nn),int)

    tmp = list(enumerate(DistancePheromoneMatrix_tmp[RandomVector[0]]))
    tmp = sorted(tmp, key=getKey)
    tmp = tmp[-nn:]
    for i in range(nn):
        nearest_neighbor[i]=tmp[i][0]
    total=0
    for i in xrange(nn):
        total+=(DistancePheromoneMatrix_tmp[RandomVector[0]][nearest_neighbor[i]])
        del i
    for i in xrange(nn):
        prob_list[i]=((DistancePheromoneMatrix_tmp[RandomVector[0]][nearest_neighbor[i]])/total)
        del i

    return nearest_neighbor,prob_list


class TwoOptSwap(object):
    def __init__(self, tour, result, distance_matrix):
        self.tour = tour
        self.result = result
        self.taboo_set = set({})
        tmp_tour = self.tour[:]
        tmp_tour_index = np.linspace(1, len(tmp_tour)-1, len(tmp_tour)-1, dtype = int)

        if len(tmp_tour) >= 4:
            while  len(self.taboo_set)  < (math.factorial(len(tmp_tour) - 1) / (2 * math.factorial(len(tmp_tour) - 3))):
                # Tabu list for random swipe
                while len(self.taboo_set)  < (math.factorial(len(tmp_tour) - 1) / (2 * math.factorial(len(tmp_tour) - 3))):
                    i, k = np.random.choice(tmp_tour_index,2, replace = False)
                    i, k = sorted([i, k])
                    if k == i + 1:
                        self.taboo_set.add((i,k))
                    elif (i,k) in self.taboo_set:
                        pass
                    else:
                        break

                # swipe two arcs
                new_tour = tmp_tour[:]
                new_tour[i:k] = tmp_tour[k-1:i-1:-1]

                # calculate new distance
                new_arc = distance_matrix[tmp_tour[i-1]][tmp_tour[k-1]] + distance_matrix[tmp_tour[i]][tmp_tour[k]]
                old_arc = distance_matrix[tmp_tour[i-1]][tmp_tour[i]] + distance_matrix[tmp_tour[k-1]][tmp_tour[k]]

                # compare the new generate distance with the old distance, and update the new route
                if new_arc <  old_arc:
                    tmp_tour = new_tour
                    self.result-= old_arc - new_arc
                    self.tour = new_tour
                    self.taboo_set = set({})
#                     print("yes")
                else:
                    self.taboo_set.add((i,k))
        else:
                pass
            
def routeToOptTwo( individual, coordination, distance_matrix, customers, depots):
    route_set = {}
    individual.get_solution()
    for depot_index, depot_tour in enumerate(individual.solution.tours):
        for route_index, route in enumerate(depot_tour): 
            path = []
            for node in route:
                path.append(node.id)
            distance = support.calDistance(path, coordination)
            route_set[distance] = path

    '''2-opt local search improvement to the final result'''
    final_result = 0
    final_set = {}
    gene_index = []
    for distance,compare_tour in route_set.items():
        improve = TwoOptSwap(compare_tour, distance, distance_matrix)
        final_set[improve.result] = improve.tour
        gene_index += improve.tour[1:-1]
        final_result += improve.result
#     support.printResult(final_set, final_result)
    
    new_individual = support.newIndividual(gene_index, customers, depots)
    return new_individual
#     tours = new_individual.get_solution().tours
#     support.printIndividualtours(tours) 
#     raw_input('prompt')