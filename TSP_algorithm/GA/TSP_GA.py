# -*- encoding: utf-8 -*-
 
import random, math, time 
import Data
from GA import GA
from matplotlib import pyplot as plt
 
class TSP(object):
    def __init__(self, city_coordinate, distance_matrix, aLifeCount = 400):
        self.city_coordinate = city_coordinate 
        self.distance_matrix = distance_matrix 
        self.lifeCount = aLifeCount
        self.every_gen_best = []
        self.ga = GA(aCrossRate = 0.8, 
              aMutationRate = 0.2,
              aLifeCount = self.lifeCount,   # the number of individual population 
              aGeneLength = len(self.city_coordinate),
              aMatchFun = self.matchFun())

    # calculate the distance between cities
    def distance(self, solution):
        total_distance = 0.0
        for (city1,city2) in zip(solution[:-1], solution[1:]):
            total_distance += self.distance_matrix[city1][city2] 
        total_distance += self.distance_matrix[solution[-1]][solution[0]]
        return total_distance
    
    # the fitness 
    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)
 
 
    def run(self, n = 0):
        iter = n
        while n > 0:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)
            self.every_gen_best.append(distance)
            if n%100 == 0:
                print ("The generation %d"%(iter-n))
#             print (("Generation times %d : distance %f") % (self.ga.generation, distance))
#             print self.ga.best.gene
            n -= 1
        print ("The end generation time %d, the best distance %f"%(self.ga.generation, distance))
#         print "The city order:",
#         print self.ga.best.gene
        total_distance = self.distance(self.ga.best.gene)
        city_result = [city_index + 1 for city_index in self.ga.best.gene]
        return city_result, total_distance 
        
        
    
def showResult(result, city_coordinate):
    x_coordination = []
    y_coordination = []
    # draw the result 
    for point in result:
        x_coordination.append(city_coordinate[point-1][0])
        y_coordination.append(city_coordinate[point-1][1])
    x_coordination.append(city_coordinate[result[0]-1][0]) # end to start
    y_coordination.append(city_coordinate[result[0]-1][1])

    plt.scatter(x_coordination,y_coordination)
    plt.plot(x_coordination,y_coordination)
    # draw the city mark
    for index in result:
        plt.text(city_coordinate[index-1][0], city_coordinate[index-1][1], index)  
    plt.text(city_coordinate[result[0]-1][0], city_coordinate[result[0]-1][1], '     Start')   #start   
    plt.text(city_coordinate[result[-1]-1][0], city_coordinate[result[-1]-1][1], '    End')   #end 
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The traveling map by GA")
    plt.show()
  
  
if __name__ == '__main__':
    cost_matrix, city_list = Data.fromTSPFile("eil51.tsp")
    cost_matrix_list = cost_matrix.matrix
    # Create an initial solution
    number_of_cities = len(city_list)
    city_coordinate = []
    

    for city in city_list:
        city_coordinate.append((city[1],city[2]))
    time_start = time.time()
    time_end = time.time()
    # solve the TSP by GA
    tsp = TSP(city_coordinate, cost_matrix_list)
    city_result, total_distance = tsp.run(200)
    time_end = time.time()
    print ('Time cost %s s.' % (time_end-time_start))
    print ('City solution:%s'% city_result)
    print ('The traveling total distance: %s' % total_distance) 
    showResult(city_result, city_coordinate)
    
    
