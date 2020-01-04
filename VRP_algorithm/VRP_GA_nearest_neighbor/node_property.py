import math

class Point(object):
    """docstring for Point"""
    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = x
        self.y = y

    def distance(self, point):
        return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

class Customer(Point):
    """docstring for Customer"""
    def __init__(self, i, x, y, d, q):
        super(Customer, self).__init__(x, y)
        self.id = i
        self.service_time = d
        self.demand = q
        self.visited = False


class Depot(Point):
    """docstring for Depot"""
    def __init__(self, i, x, y, max_dur, max_load, max_veh):
        super(Depot, self).__init__(x, y)
        self.id = i
        self.vehicle_max_duration = max_dur
        self.vehicle_max_load = max_load
        self.max_vehicle_num = max_veh

    def duration_check(self, duration):
        if self.vehicle_max_duration == float('inf'):
            return True
        else:
            return duration <= self.vehicle_max_duration
