import datamapping as dm 
import instance as inst
import algorithm as alg
import greedy_first as gf
import branchnbound as bnb
import showresult as show
import time, os

BASE_DIR = os.path.abspath('.')


def bnb_solver(instance):
    result = {}
    # import the data
    raw_data = dm.Importer()
    raw_data.import_data(instance)
    data = dm.DataMapper(raw_data)
    instance = inst.ProblemInstance(data)
    solution = alg.Solution(instance)
    # initialization 
    greedy_heuristic = gf.GreedyFirst(solution.solution)
    greedy_heuristic.run(sort=True)
    solution.value = solution.eval()
    value_from_greedy = solution.value
    # greedy solution
    print('The greedy initialization solution:')
    for i, vehicle in enumerate(greedy_heuristic.instance.fleet):
        print("vehicle "+ str(i+1)+": ", end="")
        for node in vehicle.route:
            print(node.id, end=", ")
        print('\n', end="")

    bnb_algo = bnb.BranchNBound()
    bnb_algo.initialize(instance, value_from_greedy)
    print("Starting branch&bound with initial upper_bound from greedy heuristic")
    start = time.process_time()
    upper_bound, routes, edges, times_branched = bnb_algo.run()
    end = time.process_time()
    print("time: " + str(end-start))
    print(routes)
    conv_routes = route_from_edges(routes)
    print("initial value: "+str(value_from_greedy))
    print("optimal value: "+str(upper_bound))
    print("routes:", end="")
    for i, route in enumerate(conv_routes):
        print("\nvehicle "+ str(i+1)+": ", end="")
        for node in route:
            print(node, end=", ")
    print("\n\n")
    
    show.showResult(result, raw_data.node_coordinates_list, len(raw_data.node_coordinates_list))
    
    


def route_from_edges(routes):
    DEPOT = 1
    converted_routes = []
    for route in routes:
        converted_route = []
        for edge in route:
            entry, exit = edge
            if entry not in converted_route:
                converted_route.append(entry)
            if exit not in converted_route or exit is DEPOT:
                converted_route.append(exit)
        converted_routes.append(converted_route)
    return converted_routes


if __name__ == '__main__':

    file_name = os.path.join(BASE_DIR, 'data\A-n32-k5.vrp')
    bnb_solver(file_name)
