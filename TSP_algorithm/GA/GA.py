# -*- coding: utf-8 -*-
 
import random
from Life import Life
import copy
 
last = 0
class GA(object):
    """Genetic Algorithm"""
    def __init__(self, aCrossRate, aMutationRate, aLifeCount, aGeneLength, aMatchFun = lambda life : 1):
        self.crossRate = aCrossRate               #crossover
        self.mutationRate = aMutationRate         #mutation
        self.lifeCount = aLifeCount               #the number of population
        self.geneLength = aGeneLength             #the number of cities
        self.matchFun = aMatchFun                 #the fitness
        self.lives = []                           #population
        self.best = None                          #the best individual
        self.generation = 1                       #the first generation
        self.crossCount = 0                       #the crossover times 
        self.mutationCount = 0                    #the mutation times
        self.bounds = 0.0                         #the cumulative fitness probability
        
        self.initPopulation()                     #initial the population
 
 
    def initPopulation(self):
        """Initialize the population"""
        self.lives = []
        print(self.lifeCount)
        for i in range(self.lifeCount):
            #gene = [0,1,... ,self.geneLength-1]
            #the city index
            gene = list(range(self.geneLength))
            #randomly arrange
            random.shuffle(gene)
            # a chromosome class 
            life = Life(gene)
            #put the individual in population
            self.lives.append(life)
 
 
    def judge(self):
        """calculate the fitness"""
        self.bounds = 0.0 # cumulative probability
        self.best = self.lives[0]
        for life in self.lives:
            life.score = self.matchFun(life)
            self.bounds += life.score
            # choose the best individual
            if self.best.score < life.score:
                self.best = life
 
 
    def cross(self, parent1, parent2):
        """crossover"""
        index1 = random.randint(0, self.geneLength - 1)
        index2 = random.randint(index1, self.geneLength - 1)
        tempGene = parent2.gene[index1:index2]                      
        newGene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                newGene.extend(tempGene)                               
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        self.crossCount += 1
        return newGene
 
 
    def  mutation(self, gene):
        """mutation"""
        index1 = random.randint(0, self.geneLength - 1)
        index2 = random.randint(0, self.geneLength - 1)
        gene[index1], gene[index2] = gene[index2], gene[index1]
        self.mutationCount += 1
        return gene
 
 
    def getOne(self):
        """choose individual from the parents"""
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                if life == self.best:
                    life_copy = copy.deepcopy(life)  
                    return life_copy  
                else:  
                    return life
        raise Exception("Error!", self.bounds)
    
    def getOneOther(self):
        """Copy"""
        k = 10
        num = 0
        score = []
        population = {}
        gene_list = []
        for live in self.lives:
            score.append(live.score)
            population[live.score] = live
        while num < k+1:
            max_value = max(score)
            gene_list.append(population[max_value])
            score.remove(max_value)
            num += 1
        return gene_list[random.randint(0,k)]  
#         for i in self.lives:
#             print i.score
#         raw_input('prompt')
        
 
 
    def newChild(self):
        """the offspring individual"""
        parent1 = self.getOne()
#         parent1 = self.getOneOther()
        rate = random.random()
        # decide the crossover operation
        if rate < self.crossRate:
            # crossover
            parent2 = self.getOne()
#             parent2 = self.getOneOther()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene
        # mutation
        rate = random.random()
        if rate < self.mutationRate:
            gene = self.mutation(gene)
        return Life(gene)
 
 
    def next(self):
        """generate the next"""
        self.judge() #calculate the  fitnessֵ
        newLives = []
        newLives.append(self.best) # the next generation
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1
 
             
