#!/usr/bin/env python2

import ga_vrp_deap

if __name__ == '__main__':
    ga_vrp_deap.gaVRP(
        instance_name = 'A-n32-k5', city_size = 31, pop_size = 100, cxPb = 0.8, mutPb = 0.1, Ngeneration = 10, exportCSV = False, customizeData = False)
