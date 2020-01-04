import os
import Init_parameter
BASE_DIR = os.path.abspath('.')
data_file = os.path.join(BASE_DIR, 'Augerat_1995', 'A-n32-k5.vrp') 
solution_file = os.path.join(BASE_DIR, 'Augerat_1995', 'A-n32-k5.sol')


coordination, distance_matrix, Customers, Depots, depot_lists  = Init_parameter.initParam("A-n32-k5.vrp")
