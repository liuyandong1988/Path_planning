import datamapping as dm
import math
import matplotlib.pyplot as plt 
import numpy as np
#the data file
raw_data = dm.Importer()
raw_data.import_data("A-n32-k5.vrp")
#vehicle capacity
# coordination
coordination = raw_data.node_coordinates_list 
depot = raw_data.depot

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
        z.append(coordination[i-1][0])
        w.append(coordination[i-1][1])
    for index in range(len(coordination)):
        plt.text(coordination[index][0], coordination[index][1], index+1)  
    plt.scatter(z, w, s = 100, c = "r", marker ="o", label = "Depot")
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The Best VRP ")
    plt.legend()
    plt.show()

def calDistance(route, coordination):
    distance = 0
    for index, city in enumerate(route[:-1]):
        distance += math.sqrt((coordination[city][0] - coordination[route[index+1]][0])**2 + (coordination[city][1] - coordination[route[index+1]][1])**2)
#     print distance
    return distance 

solution =  {1: [21, 31, 19, 17, 13, 7, 26], 2: [12, 1, 16, 30], 3: [27, 24], 4: [29, 18, 8, 9, 22, 15, 10, 25, 5, 20], 5: [14, 28, 11, 4, 23, 3, 2, 6]}
total_distance = 0 
for num, route in solution.items():
    route.insert(0, 0)
    route.append(0)
    distance = calDistance(route, coordination)
    total_distance += distance 
#     print route
    solution[num] = route
print 'Total distance %s' %total_distance
showResult(solution, coordination, depot)
    





 
        
