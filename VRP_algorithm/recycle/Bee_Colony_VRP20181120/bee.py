__author__ = 'Administrator'

import numpy as np
import scipy as sp
import localsearch as ls

class Bee(object):
    def __init__(self,demandlist,capacity,citylist_tabu,fitness_matrix):
        '''self attribute'''
        self.capacity = capacity          #define the bee with capacity

        '''self result'''
        self.solution_tour = []           #stores its own solution
        self.solution_path = []           #stores its path
        self.solution_distance = []
        self.result = 0                   #stores the result

        '''self variables'''
        self.demandlist = demandlist      #stores the tmp_demand_list
        self.citylist_tabu = citylist_tabu  #mark the city that it visited
        self.fitness_matrix = np.copy(fitness_matrix)

    '''single bee traveling'''
    def tourConstruction(self,citylist,distance_matrix,depot,nn):
        '''make home_depot unvisible'''
        for i in depot:
            self.fitness_matrix[:,i] = 0
            try:
                self.citylist_tabu.remove(i)
            except ValueError:
                pass
        '''starting from a random depot'''
        RandomVector = np.random.choice(depot,1)
        self.solution_tour.append(RandomVector[0])
        counter=0
        '''while bee still has capacity greater than the minimum demand somewhere'''
        while (self.capacity > min(self.demandlist) ):
            self.fitness_matrix[:,RandomVector[0]] = 0  #update the tabu list
            try:
                self.citylist_tabu.remove(RandomVector[0])     #update the tabu list
            except ValueError:
                pass
            finally:
                nearest_neighbor, prob_list = ls.nearest_neighboor( self.fitness_matrix, RandomVector, nn) # get the nearest locations to visit and the according probability

            while True:
                RandomVector = np.random.choice(nearest_neighbor, 1, p = prob_list)
                if (self.capacity - self.demandlist[RandomVector[0]] < 0) and (self.capacity > min(self.demandlist)): #if not choosing the right one, keep choosing
                    while True:
                        RandomVector = np.array(np.random.choice(citylist, 1, p=list(self.fitness_matrix[RandomVector[0]]/sum(self.fitness_matrix[RandomVector[0]]))),int)
                        if (self.capacity - self.demandlist[RandomVector[0]] < 0) and (self.capacity > min(self.demandlist)):
                            continue
                        else:
                            break
                    break
                else:
                    break
            '''update the solution'''
            self.solution_tour.append(RandomVector[0])
            self.solution_path.append((self.solution_tour[counter],self.solution_tour[counter+1]))
            self.solution_distance.append(distance_matrix[self.solution_tour[counter]][self.solution_tour[counter+1]])
            self.capacity -= self.demandlist[RandomVector[0]]
            self.demandlist[RandomVector[0]] = 99999
            counter+=1

        '''finalize the solution'''
        self.solution_distance.append(distance_matrix[self.solution_tour[-1]][self.solution_tour[0]])
        self.solution_tour.append(self.solution_tour[0])
        self.result=sum(self.solution_distance)
        del self.solution_path
        del self.solution_distance

'''using multi-bee to get 1 feasible solution'''
def solve(depot, demandlist, capacity, citylist, citylist_tabu, distance_matrix, fitness_matrix, nn):
    '''using multi-bee to solve the vrp'''
    solution_set = {}         #dictionary to store solution
    count_length = 0          #stopping factor
    result = 0
    demandlist_tmp = sp.copy(demandlist)  #make a tmp demandlist for bees to share in each fesible solution
    citylist_tabu_tmp = citylist_tabu[:]  #making a tmp tabulist for bees to share in each feasible solution
    fitness_matrix_tmp = sp.copy(fitness_matrix)        #make a tmp DistancePheromoneMatrix for bees to share in each feasible solution
    while capacity > min(demandlist_tmp):
        bee_agent = Bee(demandlist_tmp, capacity, citylist_tabu_tmp, fitness_matrix_tmp)
        bee_agent.tourConstruction(citylist, distance_matrix, depot,nn)
        demandlist_tmp = bee_agent.demandlist                                 #updating the shared tmp demandlist
        citylist_tabu_tmp = bee_agent.citylist_tabu                           #updating the shared tmp citylist_tabu
        fitness_matrix_tmp = bee_agent.fitness_matrix       #updating the shared tmp DistancePhermoneMatrix
        result += bee_agent.result
        solution_set[bee_agent.result] = bee_agent.solution_tour          #collecting the solution
        count_length += (len(bee_agent.solution_tour)-2)
    return result,solution_set

'''get multi-feasible solutions and store the best one to make an iteration'''
def iteration(compare,depot,length,demandlist,capacity,citylist,citylist_tabu,distance_matrix,fitness_matrix,population,nn):
    compare_set={}
    for i in range(population):
        result, solution_set = solve(depot, demandlist, capacity, citylist, citylist_tabu, distance_matrix, fitness_matrix,nn)
#         print 'The %i bee found the route distance %s : %s'%(i, result, solution_set)
        if result < compare:
            compare = result
            compare_set = solution_set
#             print 'The result become well %s: %s'%(result, solution_set)
        else:
            pass
    return compare, compare_set