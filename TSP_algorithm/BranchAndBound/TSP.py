#! /usr/bin/python

import Graph
import copy
from heapq import *
import matplotlib.pyplot as plt
import time
import Data


class TSPNode:
    '''
    This class represents a partial solution to the Traveling
    Salesperson Problem
    '''

    # Import a coumputeBound function and adds that as a behavior to
    # this class - allows us to easily try different computeBound
    # methods
    from computeBound import computeBound


    def __init__(self, cost_Maxtrix, aPath=[], path_length=0):
        '''
        Creates a new node with this state and bounds
        '''
        self.state = cost_Maxtrix
        self.path = copy.copy(aPath)
        self.path_length = path_length

        # Compute the new bound for this node
#         self.bound = self.computeBound()
        self.bound = None


    def addVertex(self, vertex):
        '''
        Add the given vertex to our path and compute a new bound for
        ourself
        '''

        # If we already have a start vertex, our length is the length
        # from the last node in the path to the new vertex.
        if len(self.path):
            self.path_length += self.state.getAt(self.path[-1],vertex)
        else:
            self.path_length = 0  # Redundant since it's done in init()
        # Append this new vertex to our path list
        self.path.append(vertex)
        # Compute a new bound for this node
        self.bound = self.computeBound()


    # Methods to implement relational operations between nodes based on
    # the bound - necessary so we can put nodes into a priority queue
    # and have them arranged in the proper order
    def __lt__(self, otherNode):
        return self.bound < otherNode.bound
    def __le__(self, otherNode):
        return self.bound <= otherNode.bound
    def __gt__(self, otherNode):
        return self.bound > otherNode.bound
    def __ge__(self, otherNode):
        return self.bound >= otherNode.bound


def travelingSalesperson(cost_Maxtrix):
    '''
    Find an optimal tour, if one exists, for the given graph

    Arguments:
        cost_Maxtrix - a Graph with nodes and edges

    Returns:
        (number of nodes visited, optimal tour TSPNode )
    '''
    visited_node = 0 # to keep track of how many nodes we 'visit'
    optimal_tour = None # Until we discover the first tour
    # Use a list as a priority queue ordering nodes by their bounds
    priority_queue = []
    # Starts with a root node where vertex 0 is the beginning of the
    # path and the path is empty with length 0
    current_node = TSPNode(cost_Maxtrix)
    # Add the first vertex to the existing node. This computes a new
    # bounds for this node
    current_node.addVertex(cost_Maxtrix.getNames()[0])
    # Prime the pump by pushing this initial TSPnode onto the priority
    # queue
    heappush(priority_queue, current_node)
    # While there are more nodes to explore, pop off the "best" node and
    # see if it's a solution. If so and it's better than the existing
    # best we remember it as the best. Otherwise, generate all of its
    # children by adding another vertex to the end of the path and
    # computing the bound and enqueueing the child
    while len(priority_queue) > 0 :
        # Get the "best" node off the priority queue
        current_node = heappop(priority_queue)
        # If the bound on this node looks better than current best,
        # visit, otherwise we're done!
        if not optimal_tour or (current_node.bound < optimal_tour.path_length):
            visited_node += 1
            # Check to see if we have a solution by checking to see if
            # all the nodes are part of the tour represented by this
            # node
            if len(current_node.path) == cost_Maxtrix.size():
                # Looks like we have a tour!  See if there's a path back
                # from the last node in the path to the first node in
                # the path, if so, add that edge and see if this is
                # optimal
                if cost_Maxtrix.getAt(current_node.path[-1], current_node.path[0]) != None:
                    # Complete the cyle by adding the edge back to our 
                    # beginning node
                    current_node.addVertex(current_node.path[0])
                    # Find out if this tour is shorter than the current best tour
                    if not optimal_tour or \
                          (current_node.path_length < optimal_tour.path_length):
                        # Yes it's better so it's our new optimal tour
                        optimal_tour = current_node
#                         print optimal_tour.path
#                         print optimal_tour.path_length
            else:
                # haven't found a tour yet, expand all children nodes by
                # taking the current path and adding every vertex to the
                # end where that vertex is 1) adjacent to the end and 2)
                # not already part of the path
                for node in cost_Maxtrix.getNames():
                    # If the node underconsideration is not already in
                    # our path, then is there an edge from the end of the 
                    # current path to the node under consideration? 
                    if node not in current_node.path and \
                          cost_Maxtrix.getAt(current_node.path[-1], node) != None:
                        # Add this node to the path by creating a new node with
                        # this node at the end of the path
                        newNode = TSPNode(current_node.state, 
                                          current_node.path, 
                                          current_node.path_length)
                        newNode.addVertex(node)
                        # Only enqueue this new node if its bound is better than 
                        # the current best, otherwise we just drop it
                        if not optimal_tour or \
                              (newNode.bound < optimal_tour.path_length):
                            heappush(priority_queue, newNode)

        else:  # Nothing left in priority queue is better so we're done!
            
            return visited_node, optimal_tour

    # We've explored all the nodes in the priority queue and found none
    # really better, so return the best we found.  Note that if we
    # didn't find ANY tour, then optimal_tour will be None - an
    # appropriate value to return anyway
    return visited_node, optimal_tour

#-----------------------------------------------------------------------------
def showResult(city_solution, city_coordinate):
    x_coordinate = []
    y_coordinate = []
    solution =[i-1 for i in city_solution[:-1]] # modify the path adjust to the coordinate matrix
    # draw the result 
    for city in solution:
        x_coordinate.append(city_coordinate[city][0])
        y_coordinate.append(city_coordinate[city][1])
    x_coordinate.append(city_coordinate[solution[0]][0]) # end to start
    y_coordinate.append(city_coordinate[solution[0]][1])
#         print x_coordinate 
    plt.figure(1)
    plt.scatter(x_coordinate,y_coordinate)
    plt.plot(x_coordinate,y_coordinate)
    # draw the city mark
    for city in solution:
        plt.text(city_coordinate[city][0], city_coordinate[city][1], city)  
    plt.text(city_coordinate[solution[0]][0], city_coordinate[solution[0]][1], '     Start')   #start   
    plt.text(city_coordinate[solution[-1]][0], city_coordinate[solution[-1]][1], '    End')   #end 
    plt.xlabel('City x coordinate')
    plt.ylabel("City y coordinate")
    plt.title("The traveling map by branch and bound")
    plt.grid()
    plt.show()   


if __name__ == '__main__':
    # the exact algorithm running time expensive 15 cities instance cost about 10 seconds
    an_instance, city_list = Data.fromTSPFile("eil15.tsp")
    city_coordinate = []
    for city in city_list:
        city_coordinate.append((city[1],city[2]))
    print('Running……')
    start_time = time.time()
    visited, solution = travelingSalesperson(an_instance)
    print ("Cpu time:", time.time() - start_time)
    result_path = []
    if solution:
        print ('Shortest tour is ',solution.path_length, ' long:')
        for point in solution.path:
            point += 1
            result_path.append(point)
        print (result_path)
    else:
        print ('No tour found')
    # show the map
    showResult(result_path, city_coordinate)
    
    
