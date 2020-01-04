import datamapping as dm
import point

def initParam(filename):
    #the data file
    raw_data = dm.Importer()
    raw_data.import_data(filename)
    #vehicle capacity
    capacity = int(raw_data.info["CAPACITY"])
    # coordination
    coordination = raw_data.node_coordinates_list 
    # node demand
    demand_list = raw_data.demand_array
    # distance and fitness
    distance_matrix = raw_data.distance_matrix
    # depot
    depot_lists = raw_data.depot
    depot_lists = [i-1 for i in depot_lists]
    #depot list
    Depots = []
    for depot in depot_lists:
        # [index, coordination, duration, capacity, vehicle number]
        d = point.Depot(*tuple([depot, coordination[depot][0], coordination[depot][1], None, capacity, None]))
        Depots.append(d)
    Customers = [] 
    for customer in xrange(raw_data.depot_num, raw_data.depot_num+raw_data.customer_num):
#         print customer, coordination[customer][0], coordination[customer][1], None, demand_list[customer] 
        c = point.Customer(*tuple([customer, coordination[customer][0], coordination[customer][1], None, demand_list[customer]]))
        Customers.append(c)

    return coordination, distance_matrix, Customers, Depots, depot_lists 

if __name__ == '__main__':
    coordination, distance_matrix, Customers, Depots, depot_lists = initParam("A-n32-k5.vrp")
    for depot in Depots:
        print 'The depot_id %s and max vehicle %s'%(depot.id, depot.max_vehicle_num)
    for customer in Customers:
        print 'The customer_id %s and demand %s'%(customer.id, customer.demand)
        