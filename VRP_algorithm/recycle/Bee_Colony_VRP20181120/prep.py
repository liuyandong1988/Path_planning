__author__ = 'Malakas'
import scipy as sp
import sklearn.metrics.pairwise as pairwise
import numpy as np
import matplotlib.pyplot as plt

'''cordinates generator'''
def data_clean(filename):
    '''clean data, remove headers and get the cordinates'''
    cordinates=sp.genfromtxt(filename,delimiter="")
    cordinates = cordinates[:,1:3]
    return cordinates,len(cordinates) #returns cordinates matrix and length

'''Distance Matrix Generator'''
def Distance_Matrix(cordinate,length):
    Matrix1=pairwise.pairwise_distances(cordinate, Y=None, metric='euclidean', n_jobs=1) #use to calculate Distance_Pheromone_Matrix. no round up in case 0 division occurs
    Matrix=np.around(Matrix1) #use to calculate the integer solution distance.
    for i in range(length):
        Matrix1[i][i]+=999999999
    Reverse_Matrix=(1/Matrix1)     #reverse distance
    Reverse_Matrix=np.array(Reverse_Matrix,float)
    return  Reverse_Matrix,Matrix

'''Distance_pheromone_matrix generator'''
def distance_fitness_matrix(DistanceMatrix,FitnessMatrix):
     Distance_fitness_matrix=DistanceMatrix*FitnessMatrix
     return np.array(Distance_fitness_matrix,float)

