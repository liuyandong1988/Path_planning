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
        self.duration = d
        self.demand = q

class Depot(Point):
    """docstring for Depot"""
    def __init__(self, i, x, y, max_dur, max_load, max_veh):
        super(Depot, self).__init__(x, y)
        self.id = i
        self.max_duration = max_dur
        self.max_load = max_load
        self.max_vehicle_num = max_veh

    def duration_check(self, duration):
        if self.max_duration == 0:
            return True
        else:
            return duration <= self.max_duration
