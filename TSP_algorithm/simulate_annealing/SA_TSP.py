# -*- coding: utf-8 -*-
import math, random, copy, time  
import matplotlib.pyplot as plt
import Data
        
def simuAnealling(city_count, coordinates, distance_list):
    '''
    random path and calculate distance to sreach for optimal initiate temperature
    '''
    path = [i for i in range(1,city_count+1)]# initiate path
    random.shuffle(path)
    path_new = path
    path_current = path_new
    path_best =  path_current
    distance_current = float('inf')
    distance_best = float('inf')
    each_best = []
      
    # the parameters
    T0 = 99           #initiate temperature
    Tmin = 1        # the end temperature
    T = T0
    alpha = 0.99
    kk = 1000     #times of internal circulation 
  
    # simulated annealling
    while T > Tmin:
        print ("The current temperature is:%s" %T)
        for i in range(kk):
#             print '1',path_new 
            if random.random() < 0.5:
                a = 0
                b = 0
                while a == b:
                    a = random.randint(0, city_count-1)
                    b = random.randint(0, city_count-1)
                temp = path_new[a]
                path_new[a] = path_new[b]
                path_new[b] = temp
            else:
                a = 0
                b = 0
                c = 0
                while a==b or a==c or b==c or abs(a-b) == 1 :
                    a = random.randint(0, city_count-1)
                    b = random.randint(0, city_count-1)
                    c = random.randint(0, city_count-1)
                tmp1 = a
                tmp2 = b
                tmp3 = c
                #ensure a < b < c
                if a < b and  b < c :
                    pass
                elif a < c and c < b:
                    a = tmp1; b = tmp3; c = tmp2
                elif b < a and a < c :
                    a = tmp2; b = tmp1; c = tmp3
                elif b < c and c < a :
                    a = tmp2; b = tmp3; c = tmp1
                elif c < a and a < b :
                    a = tmp3; b = tmp1; c = tmp2;
                elif c < b and b < a :
                    a = tmp3; b = tmp2; c = tmp1
                tmplist1 = path_new[a : b]
                path_new[ a : a + c - b] = path_new[b : c]
                path_new[ a + c - b : c] = tmplist1
                
            distance_new = calDistance(path_new, distance_list) 
            if distance_new < distance_current:
                distance_current = distance_new
                path_current = copy.deepcopy(path_new)
                if distance_new < distance_best:
                    distance_best = distance_new
                    path_best = copy.deepcopy(path_new)
            else:
                #metropolis principle
                p = math.exp(-(distance_new - distance_current)/T)
                if random.random() < p:
                    distance_current = distance_new
                    path_current = copy.deepcopy(path_new) 
                else:
                    path_new = copy.deepcopy(path_current)
        T = T * alpha 
        print ('Length:%s , path:%s'%(distance_best, path_best)) 
        each_best.append(distance_best)
    return path_best, each_best 


####################################################
#     # another annealing method
#     distance1=0
#     distance2=0
#     dif=0
#     for i in range(10):  
#         random.shuffle(path)
#         new_path_1 = path 
#         distance1 = calDistance(new_path_1)
#         random.shuffle(path)
#         new_path_2 = path
#         distance2 = calDistance(new_path_2)
# #         print distance1 
# #         print distance2
# #         raw_input('prompt')
#         difNew=abs(distance1-distance2)
#         if difNew>=dif:
#             dif=difNew
#     # the parameters
#     Pr = 0.5              #initiate accept possibility
#     T0 = dif/Pr           #initiate temperature
#     T = T0
#     Tmin = T/100          # the end temperature
#     kk = 10*len(path)     #times of internal circulation
#     t = 0 #time  
##############################################################

####################################################        
#         # another annealing method
#         if random.random() >= 0.85:
#             T = T*2
#             continue
#         t += 1
#         T= T0 / (1+t)
#####################################################

def calDistance(paths_list, city_distance):  # calculate the path distance
    result = 0
    for city in paths_list[0:-1]:
        result += city_distance[city-1][paths_list[paths_list.index(city)+1]-1]
    result += city_distance[paths_list[-1]-1][paths_list[0]-1]
    return result

def showResult(city_result, each_best, city_count):
    x_coordination = []
    y_coordination = []
    # draw the result 
    for point in city_result:
        x_coordination.append(city_list[point-1][1])
        y_coordination.append(city_list[point-1][2])
    x_coordination.append(city_list[city_result[0]-1][1]) # end to start
    y_coordination.append(city_list[city_result[0]-1][2])
#         print x_coordination 
    plt.figure(1)
    plt.subplot(1,2,1)
    plt.scatter(x_coordination,y_coordination)
    plt.plot(x_coordination,y_coordination)
    # draw the city mark
    for index in range(city_count):
        plt.text(city_list[index][1], city_list[index][2], city_list[index][0])  
    plt.text(city_list[city_result[0]-1][1], city_list[city_result[0]-1][2], '     Start')   #start   
    plt.text(city_list[city_result[-1]-1][1], city_list[city_result[-1]-1][2], '    End')   #end 
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The traveling map by SA")
    # draw the generation best result
    plt.subplot(1,2,2)
    plt.xlabel('Interation times')
    plt.ylabel("Total distance")
    plt.title("Simulated Annealing")
    plt.plot(each_best)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    cost_matrix, city_list = Data.fromTSPFile("eil51.tsp")
    cost_matrix_list = cost_matrix.matrix
    # Create an initial solution
    number_of_cities = len(city_list)
    city_coordination = []
    total_distance = 0

    for city in city_list:
        city_coordination.append((city[1],city[2]))
#     print city_coordination
#     print city_list
#     print cost_matrix_list
#     raw_input('prompt') 
    time_start = time.time()
    path_best, each_best = simuAnealling(number_of_cities, city_coordination, cost_matrix_list)
    time_end = time.time()
    print('The running time %s'%(time_end-time_start))
    print('The path %s'%path_best)
    showResult(path_best, each_best, number_of_cities)


