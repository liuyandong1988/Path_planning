from deap import base, creator, tools
import random
import os
from json import load
import copy
import support

def crossOver(parent1, parent2):
    """crossover by myself"""
    index1, index2 =  random.sample(xrange(0, len(parent1)), 2)
    index1, index2 = sorted([index1, index2])
    temp1 = parent2[index1:index2+1]
    temp2 = parent1[index1:index2+1]   
    copy1 = copy.deepcopy(parent1)
    copy2 = copy.deepcopy(parent2)                   
    p1len = 0
    p2len = 0
    mark_1 = 0
    mark_2 = 0
#     print '123',index1, index2, temp1, temp2 
    for g in copy1:
#         print g, p1len
        if p1len == index1:
            parent1 [index1:index2+1] = temp1                             
            p1len += (index2+1 - index1)
            mark_1 = 1
        if g not in temp1:
            parent1[p1len] = g
            p1len += 1
    if mark_1 == 0:
        parent1 [index1:index2+1] = temp1 
    for g in copy2:
#         print g, p2len
        if p2len == index1:
#             print 't2',temp2
            parent2[index1:index2+1] = temp2                           
            p2len += (index2+1 - index1)
            mark_2 = 1
        if g not in temp2:
            parent2[p2len] = g
            p2len += 1
    if mark_2 == 0:
        parent2[index1:index2+1] = temp2   
    return parent1, parent2

def cxPartialyMatched(ind1, ind2):
    """crossover by author"""
    size = min(len(ind1), len(ind2))
    p1, p2 = [0]*size, [0]*size
    # Initialize the position of each indices in the individuals
    for i in xrange(size):
        p1[ind1[i]-1] = i
        p2[ind2[i]-1] = i
    # Choose crossover points
    cxpoint1 = random.randint(0, size)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
    
    # Apply crossover between cx points
    for i in xrange(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = ind1[i]
        temp2 = ind2[i]
        # Swap the matched value
        ind1[i], ind1[p1[temp2-1]] = temp2, temp1
        ind2[i], ind2[p2[temp1-1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1-1], p1[temp2-1] = p1[temp2-1], p1[temp1-1]
        p2[temp1-1], p2[temp2-1] = p2[temp2-1], p2[temp1-1]
    
    return ind1, ind2

def mutInverseIndexes(individual):
    '''mutation'''
    start, stop = sorted(random.sample(range(1,len(individual)), 2))
#     print start, stop 
    if  random.random()  > 0.5:
        individual[:] = individual[:start] + individual[stop:start-1:-1] + individual[stop+1:]
    else:
        individual[start], individual[stop] = individual[stop], individual[start] 
    return individual,

def indDecodeRoute(individual, instance):
    '''
    individual decode the route based on the constraints
    '''
#     print individual
#     raw_input('')
    route = []
    vehicle_capacity = instance['vehicle_capacity']
    # Initialize a sub-route
    sub_route = []
    vehicle_load = 0
    for customer_id in individual:
        # Update vehicle load
        demand = instance['customer_%d' % customer_id]['demand']
        updated_vehicle_load = vehicle_load + demand
        # Validate vehicle load and elapsed time
        if updated_vehicle_load <= vehicle_capacity:
            # Add to current sub-route
            sub_route.append(customer_id)
            vehicle_load = updated_vehicle_load
        else:
            # Save current sub-route
            route.append(sub_route)
            # Initialize a new sub-route and add to it
            sub_route = [customer_id]
            vehicle_load = demand
    if sub_route != []:
        # Save current sub-route before return if not empty
        route.append(sub_route)
#     print route
#     raw_input('prompt')
    return route

def evalVRP(individual, instance):
    '''
    evaluate the individual distance
    '''
    total_cost = 0
    route = indDecodeRoute(individual, instance)
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
        # Update total cost
        total_cost = total_cost + sub_route_distance
    fitness = 1.0 / total_cost
    return fitness,


def gaVRP(instance_name, city_size, pop_size, cxPb, mutPb, Ngeneration, exportCSV = False, customizeData = False):
    '''
    The main GA code by python deap.
    '''
    if customizeData:
        jsonDataDir = os.path.join(os.path.abspath('.'),'data', 'json_customize')
    else:
        jsonDataDir = os.path.join(os.path.abspath('.'),'data', 'json')
    jsonFile = os.path.join(jsonDataDir, '%s.json' % instance_name)
    with open(jsonFile) as f:
        instance = load(f)
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register('indexes', random.sample, range(1, city_size + 1), city_size) #city_size = city_num + depot_num
    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    # Operator registering
    toolbox.register('evaluate', evalVRP, instance = instance)
    toolbox.register('select', tools.selRoulette)
    # register the crossover operator
#     toolbox.register("crossover", cxPartialyMatched)
    toolbox.register('crossover', crossOver)
    # register a mutation operator with a probability to
    toolbox.register('mutate', mutInverseIndexes)
    # Initialize the population
    pop = toolbox.population( n=pop_size )
    offspring_pop = []
    min_total_distance = float('inf')
#     # Results holders for exporting results to CSV file
#     csvData = []
    print 'Start of evolution'
    # Evaluate the entire population
    fitnesses = list(toolbox.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # Begin the evolution
    for g in range(Ngeneration):
        # Debug, suppress print()
        print '-- Generation %d --' % g
        while len(offspring_pop) != pop_size:
            parent1 = []
            parent2 = []
            # Select the next generation individuals
            parent1 = toolbox.select(pop, 1)[0]
            parent2 = toolbox.select(pop, 1)[0]
            # Clone the selected individuals
            parent1, parent2 = toolbox.map(toolbox.clone, [parent1, parent2])
#             print '1' ,set(parent1),len(set(parent1))
#             print '2', set(parent2),len(set(parent2)) 
            # Apply crossover 
            if random.random() < cxPb:
#                 print '1' ,parent1,len(set(parent1))
#                 print '2', parent2,len(set(parent2)) 
                toolbox.crossover(parent1, parent2)
                del parent1.fitness.values
                del parent2.fitness.values
#                 print '11' ,parent1,len(set(parent1))
#                 print '22', parent2,len(set(parent2)) 
            if len(set(parent1))!= city_size or len(set(parent2))!=city_size:
                raw_input('error:2')
#                 raw_input('prompt')
#             print '5' ,parent1,len(set(parent1))
#             print '6', parent2,len(set(parent2)) 
            for mutant in [parent1, parent2]:
                if random.random() < mutPb:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
#             print '55' ,parent1,len(set(parent1))
#             print '66', parent2,len(set(parent2)) 
            if len(set(parent1))!= city_size or len(set(parent2))!= city_size:
                raw_input('error:3')
#             raw_input('prompt')
            # Evaluate the individuals with an invalid fitness
            invalidInd = [ind for ind in [parent1, parent2] if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalidInd)
            for ind, fit in zip(invalidInd, fitnesses):
                ind.fitness.values = fit
                if len(offspring_pop) < pop_size:
                    offspring_pop.append(ind)
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in offspring_pop]
#         length = len(offspring_pop)
#         mean = sum(fits) / length
#         sum2 = sum(x*x for x in fits)
#         std = abs(sum2 / length - mean**2)**0.5
        max_fitness = max(fits) 
        current_min_distance = 1 / max_fitness
        if min_total_distance > current_min_distance:
            min_total_distance = current_min_distance 
            best_individual = offspring_pop[fits.index(max_fitness)] 
        pop[:] = offspring_pop
        offspring_pop = []
        print 'The current best distance %s route: %s'%(min_total_distance, best_individual)


    route = indDecodeRoute(best_individual, instance)
    route_set, total_distance = support.calDistance(route, instance)
    #---2-opt local search improvement to the final result---#
    final_set, final_result  = support.optTwo(route_set, instance['distance_matrix'])
    #---show the result----#
    route_cnt = 0
    for index, route in final_set.items():
        route_cnt += 1
        print 'From depot %s, Vehicle %s route: %s' %(route[0], route_cnt, route)  
    print 'Total distance: %s' %final_result  
    print '-- End of (successful) evolution --'
    support.showResult(final_set, instance['all_coordination'][:city_size+1], depot=[0])
