import matplotlib.pyplot as plt 
import numpy as np
import math

class TwoOptSwap(object):
    def __init__(self, tour, result, distance_matrix):
        self.tour = tour
        self.result = result
        self.taboo_set = set({})
        tmp_tour = self.tour[:]
        tmp_tour_index = np.linspace(1, len(tmp_tour)-1, len(tmp_tour)-1, dtype = int)

        if len(tmp_tour) >= 4:
            while  len(self.taboo_set)  < (math.factorial(len(tmp_tour) - 1) / (2 * math.factorial(len(tmp_tour) - 3))):
                # Tabu list for random swipe
                while len(self.taboo_set)  < (math.factorial(len(tmp_tour) - 1) / (2 * math.factorial(len(tmp_tour) - 3))):
                    i, k = np.random.choice(tmp_tour_index,2, replace = False)
                    i, k = sorted([i, k])
                    if k == i + 1:
                        self.taboo_set.add((i,k))
                    elif (i,k) in self.taboo_set:
                        pass
                    else:
                        break

                # swipe two arcs
                new_tour = tmp_tour[:]
                new_tour[i:k] = tmp_tour[k-1:i-1:-1]

                # calculate new distance
                new_arc = distance_matrix[tmp_tour[i-1]][tmp_tour[k-1]] + distance_matrix[tmp_tour[i]][tmp_tour[k]]
                old_arc = distance_matrix[tmp_tour[i-1]][tmp_tour[i]] + distance_matrix[tmp_tour[k-1]][tmp_tour[k]]

                # compare the new generate distance with the old distance, and update the new route
                if new_arc <  old_arc:
                    tmp_tour = new_tour
                    self.result-= old_arc - new_arc
                    self.tour = new_tour
                    self.taboo_set = set({})
#                     print("yes")
                else:
                    self.taboo_set.add((i,k))
        else:
                pass

def optTwo(route_set, distance_matrix):
    final_result = 0
    final_set = {}
    for distance,compare_tour in route_set.items():
        improve = TwoOptSwap(compare_tour, distance, distance_matrix)
        final_set[improve.result] = improve.tour
        final_result += improve.result
    return final_set, final_result  

#----------------plot the graph----------#
def showResult(compare_set, coordination, depot):
    print compare_set, coordination, depot
    raw_input('prompt')
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
    
def calDistance(route, instance):
    total_cost = 0
    result = {}
    for sub_route in route:
        sub_route_distance = 0
        last_customer_id = 0
        for customer_id in sub_route:
            # Calculate section distance
            distance = instance['distance_matrix'][last_customer_id][customer_id] 
            # Update sub-route distance
            sub_route_distance = sub_route_distance + distance
            # Update last customer ID
            last_customer_id = customer_id
        # Calculate transport cost
        sub_route_distance = sub_route_distance + (instance['distance_matrix'][last_customer_id][0])
        sub_route.insert(0,0)
        sub_route.append(0)
        result[sub_route_distance] = sub_route 
        # Update total cost
        total_cost = total_cost + sub_route_distance
    return result, total_cost 