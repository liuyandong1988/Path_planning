import Graph
import copy
from heapq import *
import matplotlib.pyplot as plt
import time
import numpy as np
import operator

class TSPNode:

    def __init__(self, instance, matrix, aPath=[], path_length=0, last_bound = 0):
        '''
        Creates a new node with this state and bounds
        '''
        self.last_bound = last_bound
        self.state = instance
        self.last_matrix = matrix
        self.path = copy.copy(aPath)
        self.path_length = path_length
        self.last_bound = last_bound
 

    def addVertex(self, vertex):
        self.its_matrix = []
        if len(self.path):
            self.path_length += self.state.getAt(self.path[-1],vertex)
        else:
            self.path_length = 0  # Redundant since it's done in init()
        # Append this new vertex to our path list
        self.path.append(vertex)
        # Compute a new bound for this node
        self.bound = self.computeBound()


    def computeBound(self):
        '''
        Returns a lowerbound on the optimal tour for this node
        '''
        # Use getAt to find distance between nodes
        # Sum of shortest individual paths from each node
        matrix = copy.deepcopy(self.last_matrix)
        node_value = 0
        inf_max = float('inf') 
        if len(self.path) > 1:
            delete_row,delete_colm = self.path[-2], self.path[-1] 
            node_value = matrix[delete_row,delete_colm] 
            matrix[delete_row,:] = float('inf')
            matrix[:,delete_colm] = float('inf')
            matrix[delete_colm, delete_row] = float('inf')
#             print matrix
#             print node_value
            
        row_min = []
        colm_min = []
       
        for i in xrange(len(matrix)):
            min_r = min(matrix[i, :])
#             print 'row_min', min_r
            if min_r != 0 and min_r != inf_max:
                row_min.append(min_r) 
                for j in xrange(len(matrix)):
                    if matrix[i, j] != inf_max:
                        matrix[i, j] -= min_r  
             
        for i in xrange(len(matrix)):  
            min_c = min(matrix[:, i])
            if min_c != 0 and min_c != inf_max:
                colm_min.append(min_c) 
                for j in xrange(len(matrix)):
                    if matrix[j][i] != inf_max:
                        matrix[j][i] -= min_c 
        shortest = sum(row_min) + sum(colm_min) 
        if len(self.path) == 1:
            self.last_matrix = np.array(matrix)
            self.its_matrix = np.array(matrix)
        else:
            self.its_matrix = np.array(matrix)
     
#         print self.last_matrix
#         print self.its_matrix
#         print shortest ,self.last_bound , node_value
        return (shortest + self.last_bound + node_value)

           
                        
#                         if short == None or self.state.getAt(name1, name2) < short:
#                             short = self.state.getAt(name1, name2)
#             if short:
#                 shortest += short
#         return (shortest + self.path_length)


def sortPriority(priority_queue):
    cmpfun = operator.attrgetter('bound') 
    priority_queue.sort(key = cmpfun)

    return priority_queue

        

def TSP(instance):

    start_time = time.time()
    visited_node = 0 # to keep track of how many nodes we 'visit'
    optimal_tour = None # Until we discover the first tour
    # Use a list as a priority queue ordering nodes by their bounds
    priority_queue = []
    candidate_current_node = [] 
    # Starts with a root node where vertex 0 is the beginning of the
    # path and the path is empty with length 0
    current_node = TSPNode(instance, np.array(instance.matrix))
    # Add the first vertex to the existing node. This computes a new
    # bounds for this node
    current_node.addVertex(instance.getNames()[0])
    heappush(priority_queue, current_node)
#     print current_node.bound
#     raw_input('prompt')
    # Prime the pump by pushing this initial TSPnode onto the priority
    # queue
#     heappush(priority_queue, current_node)
    # While there are more nodes to explore, pop off the "best" node and
    # see if it's a solution. If so and it's better than the existing
    # best we remember it as the best. Otherwise, generate all of its
    # children by adding another vertex to the end of the path and
    # computing the bound and enqueueing the child
#     while len(current_node.path) != len(instance.matrix) :
#         priority_queue = []
#         for node in instance.getNames():
#             if node not in current_node.path and instance.getAt(current_node.path[-1], node) != 'inf':
#                         # Add this node to the path by creating a new node with
#                         # this node at the end of the path
#                         newNode = TSPNode(current_node.state, 
#                                           current_node.last_matrix,
#                                           current_node.path, 
#                                           current_node.path_length,
#                                           current_node.bound)
#                         newNode.addVertex(node)
#                         priority_queue.append(newNode) 
#         # Get the "best" node off the priority queue
#         node_bound = min(map(lambda node: node.bound, priority_queue) ) 
#         for i,node in enumerate(priority_queue):
#             if node.bound == node_bound: 
#                 node_index = i 
#         current_node = priority_queue[node_index] 
#     return  current_node
    
    while len(priority_queue) > 0 :
        
        current_node = heappop(priority_queue)
        if len(current_node.path) == len(instance.matrix):
            if not optimal_tour or (current_node.path_length < optimal_tour.path_length):
                # beginning node
                current_node.addVertex(current_node.path[0])
                # Yes it's better so it's our new optimal tour
                optimal_tour = current_node
                continue
        candidate = []
        for node in instance.getNames():
            if node not in current_node.path and instance.getAt(current_node.path[-1], node) != 'inf':
                # Add this node to the path by creating a new node with
                # this node at the end of the path
                newNode = TSPNode(current_node.state, 
                                  current_node.last_matrix,
                                  current_node.path, 
                                  current_node.path_length,
                                  current_node.bound)
                newNode.addVertex(node)
                candidate.append(newNode) 
        if candidate != []:
            # Get the "best" node off the priority queue
            node_bound = min(map(lambda node: node.bound, candidate) ) 
            for i,node in enumerate(candidate):
                if node.bound == node_bound: 
                    priority_queue.append(node)
#                 if len(priority_queue) > 1:
#                     raw_input('prompt')
            priority_queue = sortPriority(priority_queue)
    return optimal_tour
#         if len(priority_queue) > 1:
#             raw_input('prompt')
   


def showResult(city_result, city_coordination):
    city_count = len(city_result)
    x_coordination = []
    y_coordination = []
    # draw the result 
    for point in city_result:
        x_coordination.append(city_coordination[point-1][1])
        y_coordination.append(city_coordination[point-1][2])
#     print x_coordination ,  y_coordination
    plt.figure(1)
    plt.scatter(x_coordination,y_coordination, c ='red', marker = 'o')
    plt.plot(x_coordination,y_coordination)
    # draw the city mark
    for index in xrange(city_count-1):
        plt.text(city_coordination[index][1], city_coordination[index][2], city_coordination[index][0])  
    plt.text(city_coordination[city_result[0]-1][1], city_coordination[city_result[0]-1][2], '     Start')   #start   
    plt.text(city_coordination[city_result[-2]-1][1], city_coordination[city_result[-2]-1][2], '    End')   #end 
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The traveling map by branch and bound")
    plt.grid()
    plt.show()   

if __name__ == '__main__':
    # Create a random graph with 7 vertices. 3 is the random seed for
    # populating the graph and 1.0 says it has 100% density so it's fully
    # connected - less dense graphs may or may not have a tour!
    an_instance, city_coordination = Graph.fromTSPFile("eil15.tsp")
    for i in xrange(len(an_instance.matrix  )):
        an_instance.matrix[i][i] = float('inf')
    print "The cost Matrix:%s" %an_instance.matrix    
#     an_instance = generateInstance() # paper Little 1963 instance
    # Run the Traveling Salesperson on the graph and find out how many
    # nodes we visited
    solution = TSP(an_instance)
    result_path = []
    if solution:
        print 'Shortest tour is ',solution.path_length, ' long:'
        for point in solution.path:
            point += 1
            result_path.append(point)
        print result_path
    else:
        print 'No tour found'
    # show the map
    showResult(result_path, city_coordination)