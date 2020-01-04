__author__ = 'Administrator'
import scipy as sp
import numpy as np
import bee
import localsearch as ls
import datamapping as dm
import matplotlib.pyplot as plt



def initParam(filename):
    #the data file
    raw_data = dm.Importer()
    raw_data.import_data(filename)
    #vehicle capacity
    capacity = int(raw_data.info["CAPACITY"])
    # depot
    depot = raw_data.depot
    depot = [i-1 for i in depot]
    # node demand
    demand_list = raw_data.demand_array
    for dep in depot:
        demand_list[dep] = 99999
#     print demand_list
    # citylist citylist_tabu node_num
    citylist = sp.linspace(0,len(demand_list)-1,len(demand_list))
    citylist_tabu = list(sp.copy(citylist))
    node_num = len(citylist)
    # coordination
    coordination = raw_data.node_coordinates_list 
    # distance and fitness
    distance_matrix = raw_data.distance_matrix
    fitness_matrix = []
    for row in distance_matrix:
        fitness_row = []
        for distance in row:
            if distance == 0:
                fitness = 0
            else:
                fitness = 1/distance
            fitness_row.append(fitness)
        fitness_matrix.append(fitness_row)
    return capacity, depot, demand_list, citylist, citylist_tabu, node_num, coordination, distance_matrix, fitness_matrix         

#----------------plot the graph----------#
def showResult(compare_set, coordination, depot):
    for i in compare_set:
        tour = compare_set[i]
        x = []
        y = []
        for j in tour:
            x.append(coordination[j][0])
            y.append(coordination[j][1])
            random_color = [ i[0] for i in np.random.rand(3,1)]
            plt.scatter(x, y, c = random_color, marker ="*")
            plt.plot(x, y, c = random_color)
    z = []
    w = []
    for i in depot:
        z.append(coordination[i][0])
        w.append(coordination[i][1])
    for index in range(len(coordination)):
        plt.text(coordination[index][0], coordination[index][1], index+1)  
    plt.scatter(z, w, s = 100, c = "r", marker ="o", label = "Depot")
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The VRP map by Bee")
    plt.legend()
    plt.show()
#-----------------Solve VRP using ABC-Meta-Heuristic-----------#
def beeHeuristic(capacity, depot, demand_list, citylist, citylist_tabu, node_num, coordination, distance_matrix, fitness_matrix):
    iterations, population = 3, 100
    local_search, lamada, nn = "on", 1.2, 1
    compare_result = float('inf')
    waggle_dance=0
    reverse_distance_matrix = fitness_matrix 
    for iter in range(iterations):
        '''run with multi replications to determine the iteration best result'''
        result_iter,tour_set_iter = bee.iteration(compare_result, depot, node_num, demand_list, capacity, citylist, citylist_tabu, distance_matrix,
                                                fitness_matrix, population, nn)
    
        if result_iter < compare_result:
            compare_result = result_iter
            compare_set = tour_set_iter
        else:
            pass
        print("iteration %i: "%iter,compare_result)
    
        '''waggle_dance'''
        for i in tour_set_iter:
            for count in xrange(len(tour_set_iter[i])-1):
                fitness_matrix[tour_set_iter[i][count]][tour_set_iter[i][count+1]] *=lamada #updata delta_tao matrix
                #fitness_matrix[compare_set[i][count+1]][compare_set[i][count]] *=lamada
        waggle_dance += 1
        if waggle_dance > 50:
            fitness_matrix = reverse_distance_matrix
            waggle_dance = 0
        else:
            pass
    
    '''2-opt local search improvement to the final result'''
    final_set = {}
    final_result = 0
    if local_search=="on":
        compare_tour = compare_set[i]
        length = len(compare_tour)
        improve = ls.TwoOptSwap(compare_tour,i,distance_matrix)
        print (compare_tour,i,distance_matrix)
        input('prompt')
        final_set[improve.result] = improve.tour
        final_result += improve.result
    else:
        final_set = compare_set
        final_result = compare_result
    
    route_num = 0
    for distance, route in final_set.items():
        route_num += 1 
        print 'Route #%s: %s'%(route_num, route)
    print 'Cost %s'%final_result
    

    '''plot'''
    showResult(final_set, coordination, depot)

if __name__ == '__main__':
    filename = "A-n32-k5.vrp"
    capacity, depot, demand_list, citylist, citylist_tabu, node_num, coordination, distance_matrix, fitness_matrix = initParam(filename)
    beeHeuristic(capacity, depot, demand_list, citylist, citylist_tabu, node_num, coordination, distance_matrix, fitness_matrix)
    
    
