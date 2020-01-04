import math
import mdvrp_ga
import matplotlib.pyplot as plt 
import numpy as np

def calDistance(route, coordination):
    '''
    calculate the distance between cities
    '''
    distance = 0
    for index, city in enumerate(route[:-1]):
        distance += math.sqrt((coordination[city][0] - coordination[route[index+1]][0])**2 + (coordination[city][1] - coordination[route[index+1]][1])**2)
#     print distance
    return distance 


#---show the result----#
def printResult(final_set, final_result):
    route_cnt = 0
    for index, route in final_set.items():
        route_cnt += 1
        print ('From depot %s, Vehicle %s route: %s' %(route[0], route_cnt, route))
    print ('Total distance: %s' %final_result)
    
def printIndividualtours(tours):
    vehicle = 0
    for depot_index, depot_tour in enumerate(tours):
        for route_index, route in enumerate(depot_tour): 
            path = []
            vehicle += 1
            for node in route:
                path.append(node.id)
            print ('The vehicle %s and route: %s'%(vehicle, path))
            
#---generate the new individual  
def newIndividual(gene_index, customers, depots):
    genes = [[] for _ in range(len(depots))]
    for city_id in gene_index:
        for customer in customers:
            if customer.id == city_id:
                genes[0].append(customer)
                break
    new_individual = mdvrp_ga.Chromosome(genes, customers, depots)
    return new_individual

def popInformation(population):
    min_fitness = population[0].get_solution().total_distance
    avg_fitness = 0
    for i in range(len(population)):
        avg_fitness += population[i].get_solution().total_distance
    avg_fitness /= len(population)
    print('Avg Fit:', avg_fitness)
    print('Min Fit:', min_fitness)

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
    plt.title("The VRP map by GA")
    plt.legend()
    plt.show()