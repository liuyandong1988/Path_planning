import import_data
import os, math
import tsp2opt
from matplotlib import pyplot as plt
import numpy as np


class SweepAlgorithm(object):

    def __init__(self, vehicle_capacity, demand_list, coordinates, distance_matrix):
        self.v_capacity = vehicle_capacity
        self.c_demand = demand_list
        self.coordinates = coordinates
        self.distance_matrix = distance_matrix
        self.polar_sort()

    def polar_sort(self):
        d_coordinate = self.coordinates[0]
        c_coordinates = self.coordinates[1:]
        node_id = 1
        self.store_info = list()
        for c_coordinate in c_coordinates:
            angle_tmp = math.atan((c_coordinate[1]-d_coordinate[1])/(c_coordinate[0]-d_coordinate[0]))
            if c_coordinate[1]-d_coordinate[1] < 0:
                if angle_tmp > 0:
                    angle_tmp = -math.pi + angle_tmp
                else:
                    pass

            else:
                if angle_tmp > 0:
                    pass
                else:
                    angle_tmp = math.pi + angle_tmp
            raddi_tmp = self.cal_distance(c_coordinate, d_coordinate)
            self.store_info.append([node_id, angle_tmp, raddi_tmp])
            node_id += 1
        # sorting increase
        self.store_info.sort(key=lambda x: x[1], reverse=False)
        print('Sorting:', self.store_info)

    def cal_distance(self, my_node1, my_node2):
        x1, y1 = my_node1
        x2, y2 = my_node2
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance

    def run(self):
        """
        cluster based on the polar
        :return:
        """
        tmp_capacity = 0
        route_id = 1
        route_node = list()
        all_route = dict()
        new_route_mark = False
        while self.store_info:
            if new_route_mark:
                new_route_mark = False
            else:
                node = self.store_info.pop(0)
            tmp_capacity += self.c_demand[node[0]]
            if tmp_capacity <= self.v_capacity:
                route_node.append(node[0])
            else:
                # print('Capacity constraint！')
                # generate a route
                all_route[route_id] = route_node
                # reset new route
                route_id += 1
                route_node = list()
                tmp_capacity = 0
                new_route_mark = True
        # the last route
        all_route[route_id] = route_node
        # optimal the each route by 2-opt
        result_routes = dict()
        for route_id, route in all_route.items():
            route.append(0)
            num_cities = len(route)
            coordinate = [self.coordinates[i] for i in route]
            tsp_route = tsp2opt.two_opt_algorithm(num_cities, coordinate, self.distance_matrix)
            tmp_route = [route[i] for i in tsp_route]
            depot_index = tmp_route.index(0)
            if depot_index+1 == len(tmp_route):
                opt_route = [0] + tmp_route
            else:
                opt_route = tmp_route[tmp_route.index(0):] + tmp_route[:tmp_route.index(0)+1]
            # print(tsp_route)
            # print(opt_route)
            result_routes[route_id] = opt_route
        return result_routes


# ---show the result----#
def print_result(results, distance_matrix):
    route_cnt = 0
    total_distance = 0
    for key, route in results.items():
        total_distance += sum(distance_matrix[i][j] for i, j in zip(route[:-1], route[1:]))
        print('Route %s: %s' % (key, route))
    print('Total distance: %s' % total_distance)


#----------------plot the graph----------#
def show_result(all_routes, coordination):
    for index, route in all_routes.items():
        x = []
        y = []
        # add depot as start and end point
        for j in route:
            x.append(coordination[j][0])
            y.append(coordination[j][1])
            random_color = [i[0] for i in np.random.rand(3, 1)]
            plt.scatter(x, y, c=random_color, marker="*")
            plt.plot(x, y, c=random_color)
    # depot
    z = []
    w = []
    z.append(coordination[0][0])
    w.append(coordination[0][1])
    for index in range(len(coordination)):
        plt.text(coordination[index][0], coordination[index][1], index)
    plt.scatter(z, w, s=100, c="r", marker="o", label="Depot")
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The VRP map by sweep algorithm")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    BASE_DIR = BASE_DIR = os.path.abspath('.')
    file_name = os.path.join(BASE_DIR, 'data\A-n45-k6.vrp')
    vehicle_capacity, demand_list, coordinates, distance_matrix = import_data.initData(file_name)
    instance_vrp_sweep = SweepAlgorithm(vehicle_capacity, demand_list, coordinates, distance_matrix)
    opt_result = instance_vrp_sweep.run()
    print_result(opt_result, distance_matrix)
    show_result(opt_result, coordinates)

    # instance
    # A-n32-k5.vrp
    # A-n45-k6.vrp
    # A-n55-k9.vrp
    # A-n69-k9.vrp
    # A-n80-k10.vrp
