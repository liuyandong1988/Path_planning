import random
import math

import time


def dist(x0,x1,y0,y1):
    return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)

#-----------------------------------------------------------------------------
def length(n1, n2):
    """Compute the distance between two nodes"""
    return dist(n1[0], n2[0],n1[1],n2[1])
#-----------------------------------------------------------------------------
#
#    Before 2opt             After 2opt
#       Y   Z                    Y   Z
#       O   O----->              O-->O---->
#      / \  ^                     \
#     /   \ |                      \
#    /     \|                       \
# ->O       O              ->O------>O
#   C       X                C       X
#
# In a 2opt optimization step we consider two nodes, Y and X.  (Between Y
# and X there might be many more nodes, but they don't matter.) We also
# consider the node C following Y and the node Z following X. i
#
# For the optimization we see replacing the edges CY and XZ with the edges CX
# and YZ reduces the length of the path  C -> Z.  For this we only need to
# look at |CY|, |XZ|, |CX| and |YZ|.   |YX| is the same in both
# configurations.
#
# If there is a length reduction we swap the edges AND reverse the direction
# of the edges between Y and X.
#
# In the following function we compute the amount of reduction in length
# (gain) for all combinations of nodes (X,Y) and do the swap for the
# combination that gave the best gain.
#

def optimize2opt(solution, number_of_nodes, city_coordinate):
#     print ('1', solution)
    best = 0
    best_move = None
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
#             print c,y,x,z
           
            # Compute the lengths of the four edges.
            cy = length( city_coordinate[c], city_coordinate[y] ) 
            xz = length( city_coordinate[x], city_coordinate[z] )
            cx = length( city_coordinate[c], city_coordinate[x] )
            yz = length( city_coordinate[y], city_coordinate[z] )
#             print cy, xz, cx, yz  
        
            # Only makes sense if all nodes are distinct
            if xi != ci and xi != yi:
                # What will be the reduction in length.
                gain = (cy + xz) - (cx + yz)
                # Is is any better then best one sofar?
                if gain > best:
                    # Yup, remember the nodes involved
                    best_move = (ci,yi,xi,zi)
                    best = gain
#     print best, best_move
#     print solution
    if best_move is not None:
#         print '1', calcLength(solution)
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
#         print '2', calcLength(new_solution)
        return True,new_solution
    else:
        return False,solution

#-----------------------------------------------------------------------------
def calcLength(solution, distance_matrix):
    total_distance = 0
#     print solution
    for (city1,city2) in zip(solution[:-1], solution[1:]):
#         print city1,city2 
        total_distance += distance_matrix[city1][city2] 
    total_distance += distance_matrix[solution[-1]][solution[0]]
    return total_distance  
#-----------------------------------------------------------------------------
def two_opt_algorithm(number_of_cities, city_coordinate, distance_matrix):
    """
    input:
    number_of_cities, the number of cities
    city_coordinate: the coordinate of cities
    distance_matrix: distance matrix
    """
    
    #the city index
    solution = list(range(number_of_cities))
            #randomly arrange
    random.shuffle(solution)
#     print solution
    go = True
    times = 0
    # Try to optimize the solution with 2opt until
    # no further optimization is possible.
    while go:
        times += 1
        go,solution = optimize2opt(solution, number_of_cities, city_coordinate)
        length = calcLength(solution, distance_matrix)
#         print (times, length)
    return solution     

