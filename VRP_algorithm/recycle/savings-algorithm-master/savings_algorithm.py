#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:28:35 2019

@author: gaz
"""

import pandas as pd
import numpy as np


df = pd.read_csv("scm_1.csv",header=None);

matrix = df.to_numpy()
matrix = matrix[1:,1:]
matrix = np.where(np.isnan(matrix), 0, matrix)

#got half filled matrix
distance_matrix = matrix
num_rows = matrix.shape[0]
    
#fully filled matrix for easier access
for i in range(num_rows):
    for j in range(i, num_rows):
        distance_matrix[i][j] = matrix[j][i]
        
routes = [[1,2,3,4,5,6],
          [7,8,9,10,11],
          [12,13,14,15,16,17],
          [18,19,20,21,22],
          [23,24,25,26,27],
          [28,29,30,31,32,33]]

route_numbers = 1;
for route in routes:
    #eg. route = [1,2,3,4,5,6] or [7,8,9,10,11]
    print("route",route_numbers)
    route_numbers+=1
    r1 = route[0]
    r2 = route[-1]+1
    society_matrix = matrix[r1:r2,r1:r2]
    #eg. matrix[0:6, 0:6]

    #Calculate savings matrix
    
    savings_matrix = np.zeros((r2-r1,r2-r1))
    for i in range(r1,r2):
        for j in range(r1,r2):
            if i==j:
                continue
            savings_matrix[i-r1][j-r1] = distance_matrix[0][i] + distance_matrix[0][j] - distance_matrix[i][j]
           
    print(savings_matrix)