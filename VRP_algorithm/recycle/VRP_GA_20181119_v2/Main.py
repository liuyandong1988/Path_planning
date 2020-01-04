import Init_parameter
import InitPopulation
import mdvrp_ga as ga
import support

def main():
    coordination, distance_matrix, Customers, Depots, depot_lists  = Init_parameter.initParam("A-n32-k5.vrp")
    iteration = 10
    pop_size = 50
    population = InitPopulation.initialPopulation(Customers, Depots, pop_size, distance_matrix)
    ga.sortPop(population)
#     for indi in population:
#         aa = []
#         for node in indi.genes[0]:
#             aa.append(node.id)
#         print 'Inidividual  and genes:%s'%( aa)
    for i in range(iteration):
        population = ga.geneticAlgorithm(population, pop_size, coordination, distance_matrix, Customers, Depots)
        print('Gen ', i+1)
        support.popInformation(population)
        print('-----------------')
        
    #--- result----#
    route_set = {}
    route_result = 0
    individual = population[0]
    for depot_index, depot_tour in enumerate(individual.solution.tours):
        for route_index, route in enumerate(depot_tour): 
            path = []
            for node in route:
                path.append(node.id)
            distance = support.calDistance(path, coordination) 
            route_result += distance
            route_set[distance] = path
    support.printResult(route_set, route_result )
    support.showResult(route_set, coordination, depot_lists)

if __name__ == '__main__':
    '''
    GA nearest neighbor initial and use 2-opt vrp
    '''
    main()