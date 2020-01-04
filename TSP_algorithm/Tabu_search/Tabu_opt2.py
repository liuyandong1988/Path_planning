# -*- coding: utf-8 -*-
import math
import random
import matplotlib.pyplot as plt
import copy, Data

def calTotalDistance(paths_list, city_distance):  # calculate the path distance
    result = 0
    for city in paths_list[0:-1]:
        result += city_distance[city][paths_list[paths_list.index(city)+1]]
    result += city_distance[paths_list[-1]][paths_list[0]]
    return result
        

class TabuSearch(object):
    '''   
    '''
    def __init__(self, distance_matrix, city_count, origin_time, tabu_length):
        self.origin_time = origin_time
        self.tabu_length = tabu_length  
        self.final_road = [] # the result route
        self.final_cost = [] # the total distance of route
        self.distance_matrix = distance_matrix
        self.city_count = city_count   


    def dist(self, x0,x1,y0,y1):
        return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
    #-----------------------------------------------------------------------------
    def length(self, n1, n2):
        """Compute the distance between two nodes"""
        return self.dist(n1[0], n2[0],n1[1],n2[1]) 

    # put the moving in the tabu list 
    def addTabu(self, road_distance):  
        self.tabu_cost.append(road_distance)
        self.tabu_move_list.append(self.tabu_object)
        if len(self.tabu_cost) > self.tabu_length :
            del self.tabu_cost[0]
            del self.tabu_move_list[0]

    def performMove(self, best_move, solution, number_of_nodes):
        (ci,yi,xi,zi) = best_move
        # Create an empty solution
        new_solution = list(range(0,number_of_nodes))
        # In the new solution C is the first node.
        # This we we only need two copy loops instead of three.
        new_solution[0] = solution[ci]

        n = 1
        # Copy all nodes between X and Y including X and Y
        # in reverse direction to the new solution
        while xi != yi:
            new_solution[n] = solution[xi]
            n = n + 1
            xi = (xi-1)%number_of_nodes
        new_solution[n] = solution[yi]
       
        n = n + 1
        # Copy all the nodes between Z and C in normal direction.
        while zi != ci:
            new_solution[n] = solution[zi]
            n = n + 1
            zi = (zi+1)%number_of_nodes
#         print new_solution 
        self.tabu_object = best_move 
        road_distance = calTotalDistance(new_solution, self.distance_matrix)
        self.addTabu(road_distance)
        return True, new_solution
        
    def check_aspiration_criteria(self, solution, best_move , number_of_nodes):
        new_route = copy.deepcopy(solution)
        mark, new_solution = self.performMove(best_move, new_route, number_of_nodes)
        new_route_value = calTotalDistance(new_solution, self.distance_matrix)
        if new_route_value < self.tabu_cost[self.tabu_move_list.index(self.tabu_object)]:
            return True
        else:
            return False
        
    #-----------------------------------------------------------------------------
    def optimize2opt(self, solution, number_of_nodes, city_list):
        best = 0
        best_move = None
        city_coordination = []
        for city in city_list:
            city_coordination.append([int(city[1]),int(city[2])])
        # For all combinations of the nodes
        for ci in range(0, number_of_nodes):
            for xi in range(0, number_of_nodes):
                yi = (ci + 1) % number_of_nodes  # C is the node before Y
                zi = (xi + 1) % number_of_nodes  # Z is the node after X
    #             print ci, yi, xi,  zi
     
                c = solution[ ci ]
                y = solution[ yi ]
                x = solution[ xi ]
                z = solution[ zi ]
#                 print c,y,x,z
               
                # Compute the lengths of the four edges.
                cy = self.length( city_coordination[c], city_coordination[y] ) 
                xz = self.length( city_coordination[x], city_coordination[z] )
                cx = self.length( city_coordination[c], city_coordination[x] )
                yz = self.length( city_coordination[y], city_coordination[z] )
#                 print cy, xz, cx, yz  
            
                # Only makes sense if all nodes are distinct
                if xi != ci and xi != yi:
                    # What will be the reduction in length.
                    gain = (cy + xz) - (cx + yz)
                    # Is is any better then best one so far?
                    if gain > best:
                        # Yup, remember the nodes involved
                        best_move = (ci,yi,xi,zi)
                        best = gain
#         print best, best_move
    #     print solution
        if best_move is not None:
            if best_move not in self.tabu_move_list:
#                 print '1',calTotalDistance(solution)  
                mark, new_solution = self.performMove(best_move, solution, number_of_nodes)
#                 print '2',calTotalDistance(new_solution), new_solution
                return mark, new_solution
            else:
                if self.check_aspiration_criteria(solution, best_move, number_of_nodes):
                    change_index = self.tabu_move_list.index(self.tabu_object)
                    del self.tabu_cost[change_index]
                    del self.tabu_move_list[change_index]
                    mark, new_solution = self.performMove(best_move, solution, number_of_nodes)
                    return mark, new_solution
                else:
                    # Generate a jump solution
                    temp = solution[:len(solution)//2]
                    solution = solution[len(solution)//2:]  +  temp
                    return True, solution 
        else:
            return False,solution

        
    #running 
    def run(self):
        road_distance = float('inf')
        for origin in range(self.origin_time):
            print ('The origin times:%s, best distance:%s'%(origin, road_distance))  
            road = [i for i in range(self.city_count)]
            random.shuffle(road)
#             print 'Road:%s'%road
            self.tabu_cost = [] # put the best cost
            self.tabu_move_list = []  # Tabu list
          
            go = True
            times = 0
            # Try to optimize the solution with 2opt until
            # no further optimization is possible.
            while go:
                times += 1
                go,road = self.optimize2opt(road, self.city_count, city_list)
#                 print times, calTotalDistance(road) 
#             raw_input('prompt')
            self.final_road.append(road)
            road_distance = calTotalDistance(road, self.distance_matrix)
            self.final_cost.append(road_distance)
#         print self.final_road 
#         print self.final_cost 
        result_best_value = min(self.final_cost) 
        result_best_road = self.final_road[self.final_cost.index(min(self.final_cost))]
        print ('The best distance is %s road %s.'%(result_best_value, result_best_road))
        return result_best_road 

def show_result(result, city_coordinate):
    x_coordination = []
    y_coordination = []
    # draw the result 
    # result includes the zero node
    for point in result:
        x_coordination.append(city_coordinate[point][0])
        y_coordination.append(city_coordinate[point][1])
    x_coordination.append(city_coordinate[result[0]][0]) # end to start
    y_coordination.append(city_coordinate[result[0]][1])
    plt.scatter(x_coordination,y_coordination)
    plt.plot(x_coordination,y_coordination)
    # draw the city mark
    for index in range(len(result)):
        plt.text(city_coordinate[index][0], city_coordinate[index][1], index)  
    plt.text(city_coordinate[result[0]][0], city_coordinate[result[0]][1], '     Start')   #start   
    plt.text(city_coordinate[result[-1]][0], city_coordinate[result[-1]][1], '    End')   #end 
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The traveling map by Tabu")
    plt.show()
    
    
if __name__ == '__main__':
    cost_matrix, city_list = Data.fromTSPFile("eil101.tsp")
    cost_matrix_list = cost_matrix.matrix
    # Create an initial solution
    number_of_cities = len(city_list)
    city_coordination = []
    for city in city_list:
        city_coordination.append((city[1],city[2]))
    tabuSearch = TabuSearch(cost_matrix_list, number_of_cities, origin_time = 10, tabu_length = 50)
    result = tabuSearch.run()
    show_result(result, city_coordination)