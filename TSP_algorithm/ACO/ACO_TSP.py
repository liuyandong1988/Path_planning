# -*- coding: UTF-8 -*-
'''
程序主体：
类AntColony的实例化->类BACA的初始化->执行BACA.ReadCityInfo()方法->执行BACA.Search()方法->执行BACA.PutAnts()方法
->类ANT的初始化->类ANT的实例化->执行ANT.MoveToNextCity()方法->执行ANT.SelectNextCity()方法->执行ANT.AddCity()方法
->执行ANT.UpdatePathLen()方法->执行BACA.UpdatePheromoneTrail()方法

蚁群算法中关键两个问题，一个是选择下一个城市的算法，主要在ANT.SelectNextCity(self, alpha, beta)方法中，其中alpha为表征
信息素重要程度的参数，beta为表征启发式因子重要程度的参数；而更新信息素主要在BACA.UpdatePheromoneTrail(self)方法中。
'''

import os,time
import sys
import random  
from math import *
import pylab as pl
import pandas as pd
from docutils.nodes import row
from matplotlib import pyplot as plt
import Data







class AntColony:  # 定义类BACA，执行蚁群基本算法

    def __init__(self, number_of_cities, city_set, cost_matrix_list, antCount, nMax, q=80, alpha=2, beta=5, rou=0.4):
        self.city_count = number_of_cities  # the cities
        self.city_set = city_set # sets数据类型是个无序的、没有重复元素的集合，两个sets之间可以做差集
        self.distance_matrix = cost_matrix_list  
        self.best_route = list() # 用于放置最佳路径选择城市的顺序
        self.AntCount = antCount  # ants
        self.Q = q  # 信息素增加强度系数
        self.Alpha = alpha  # 表征信息素重要程度的参数
        self.Beta = beta  # 表征启发因子重要程度的参数
        self.Rou = rou  # 信息素蒸发系数
        self.Nmax = nMax  # 最大迭代次数
        self.Shortest = 10e6  # 初始最短距离应该尽可能大，至少大于估算的最大城市旅行距离
        self.every_best = []
        self.pheromone_trail_list = list()  # 信息素列表（矩阵）
        self.pheromone_delta_trail_list = list()  # 释放信息素列表（矩阵）
        random.seed()  # 设置随机种子
        # 初始化全局数据结构及值
        # 循环城市总数的次数（即循环range(0,51),为0-50，不包括51）
        for nCity in range(self.city_count):
            self.best_route.append(0)  # 设置最佳路径初始值均为0
        for row in range(self.city_count):  # 再次循环城市总数的次数
            pheromoneList = []  # 定义空的信息素列表
            pheromoneDeltaList = []  # 定义空的释放信息素列表
            for col in range(self.city_count):  # 循环城市总数的次数
                pheromoneList.append(100)  # 定义一个城市到所有城市路径信息素的初始值
                pheromoneDeltaList.append(0)  # 定义一个城市到所有城市路径释放信息素的初始值
            # 建立每个城市到所有城市路径信息素的初始值列表矩阵
            self.pheromone_trail_list.append(pheromoneList)
            # 建立每个城市到所有城市路径释放信息素的初始值列表矩阵
            self.pheromone_delta_trail_list.append(pheromoneDeltaList)
#         print pheromoneList
#         print len(self.pheromone_trail_list)
#         print self.pheromone_trail_list
#         raw_input('prompt')

    def PutAnts(self):  # 定义蚂蚁所选择城市以及将城市作为参数定义蚂蚁的方法和属性
        self.ant_list = []  # 蚂蚁列表
        for antNum in range(self.AntCount):  # 循环蚂蚁总数的次数
            city = random.randint(1, self.city_count)  # 随机选择一个城市
            ant = ANT(self.city_set, self.distance_matrix, self.pheromone_trail_list, city)  # 蚂蚁类ANT的实例化，即将每只蚂蚁随机选择的城市作为传入的参数，使之具有ANT蚂蚁类的方法和属性
            self.ant_list.append(ant)  # 将定义的每只蚂蚁追加到列表中
#             print antNum, city

    def Search(self):  # 定义搜索最佳旅行路径方法的主程序
        for iter in range(self.Nmax):  # 循环指定的迭代次数
            self.PutAnts()  # 执行self.PutAnts()方法，定义蚂蚁选择的初始城市和蚂蚁具有的方法和属性

            for ant in self.ant_list:  # 循环遍历蚂蚁列表，由self.PutAnts()方法定义获取
                for ttt in range(self.city_count):  # 循环遍历城市总数次数
                    # 执行蚂蚁的ant.MoveToNextCity()方法，获取蚂蚁每次旅行时的旅行路径长度CurrLen，禁忌城市城市列表TabuCityList等属性值
                    ant.MoveToNextCity(self.Alpha, self.Beta)
#                 print ant.TabuCitySet
#                 print ant.TabuCityList
                ant.two_opt_search()  # 使用邻域优化算法    $$$
                ant.UpdatePathLen()  # 使用ant.UpdatePathLen更新蚂蚁旅行路径长度
            tmpLen = self.ant_list[0].CurrLen  # 将蚂蚁列表中第一只蚂蚁的旅行路径长度赋值给新的变量tmplen
            # 将获取的蚂蚁列表的第一只蚂蚁的禁忌城市列表赋值给新的变量tmpTour
            tmpTour = self.ant_list[0].TabuCityList
            for ant in self.ant_list[1:]:  # 循环遍历蚂蚁列表，从索引值1开始，除第一只外
                # 如果循环到的蚂蚁旅行路径长度小于tmpLen即前次循环蚂蚁旅行路径长度，开始值为蚂蚁列表中第一只蚂蚁的旅行路径长度
                if ant.CurrLen < tmpLen:
                    tmpLen = ant.CurrLen  # 更新变量tmpLen的值
                    tmpTour = ant.TabuCityList  # 更新变量tmpTour的值，即更新禁忌城市列表
            if tmpLen < self.Shortest:  # 如果从蚂蚁列表中获取的最短路径小于初始化时定义的长度
                self.Shortest = tmpLen  # 更新旅行路径最短长度
                self.best_route = tmpTour  # 更新初始化时定义的最佳旅行城市次序列表
            # 打印当前迭代次数、最短旅行路径长度和最佳旅行城市次序列表
            self.every_best.append(self.Shortest)
            print(iter, ":", self.Shortest, ":", self.best_route)
            # 完成每次迭代需要使用self，UpdatePheromoneTrail()方法更新信息素
            self.UpdatePheromoneTrail()
        return self.Shortest, self.best_route 


    def UpdatePheromoneTrail(self):  # 定义更新信息素的方法，需要参考前文对于蚁群算法的阐述
        for ant in self.ant_list:  # 循环遍历蚂蚁列表
            for city in ant.TabuCityList[0:-1]:  # 循环遍历蚂蚁的禁忌城市列表
                idx = ant.TabuCityList.index(city)  # 获取当前循环 禁忌城市的索引值
                nextCity = ant.TabuCityList[idx + 1]  # 获取当前循环禁忌城市紧邻的下一个禁忌城市
                self.pheromone_delta_trail_list[
                    city - 1][nextCity - 1] += self.Q / ant.CurrLen
                # 逐次更新释放信息素列表，注意矩阵行列所代表的意义，[city-1]为选取的子列表即当前城市与所有城市间路径的
                # 释放信息素值，初始值均为0，[nextCity-1]为在子列表中对应紧邻的下一个城市，释放信息素为Q，信息素增加强度
                # 系数与蚂蚁当前旅行路径长度CurrLen的比值，路径长度越小释放信息素越大，反之则越小。
                self.pheromone_delta_trail_list[
                    nextCity - 1][city - 1] += self.Q / ant.CurrLen
                # 在二维矩阵中，每个城市路径均出现两次，分别为[city-1]对应的[nextCity-1]和[nextCity-1]对应的[city-1]，因此都需要更新，
                # 注意城市序列因为从1开始，而列表索引值均从0开始，所以需要减1
            lastCity = ant.TabuCityList[-1]  # 获取禁忌城市列表的最后一个城市
            firstCity = ant.TabuCityList[0]  # 获取禁忌城市列表的第一个城市
            self.pheromone_delta_trail_list[
                lastCity - 1][firstCity - 1] += self.Q / ant.CurrLen
            # 因为蚂蚁旅行需要返回开始的城市，因此需要更新禁忌城市列表最后一个城市到第一个城市旅行路径的释放信息素值，即最后一个城市对应第一个城市的释放信息素值
            self.pheromone_delta_trail_list[
                firstCity - 1][lastCity - 1] += self.Q / ant.CurrLen
#             print self.pheromone_delta_trail_list
#             raw_input('prompt')
            # 同理更新第一个城市对应最后一个城市的释放信息素值

        for city1 in range(1, self.city_count+1):  # 循环遍历城市列表，主要是提取city1即城市的序号
            # 再次循环遍历城市列表，主要是提取city2即城市序号，循环两次的目的仍然是对应列表矩阵的数据结构
            for city2 in range(1, self.city_count+1):
                self.pheromone_trail_list[city1 - 1][city2 - 1] = ((1 - self.Rou) * self.pheromone_trail_list[
                                                            city1 - 1][city2 - 1] + self.pheromone_delta_trail_list[city1 - 1][city2 - 1])
                # 将释放信息素列表值再次初始化为0，用于下次循环
                self.pheromone_delta_trail_list[city1 - 1][city2 - 1] = 0
# print(self.pheromone_trail_list)


class ANT:  # 定义蚂蚁类，使得蚂蚁具有相应的方法和属性

    def __init__(self, city_set, distance_matrix, pheromone_trail_list, currCity=0):  # 蚂蚁类的初始化方法，默认传入当前城市序号为0
        self.city_set = city_set 
        self.distance_matrix = distance_matrix 
        self.TabuCitySet = set()
        self.pheromone_trail_list = pheromone_trail_list 
        # 定义禁忌城市集合，定义集合的目的是集合本身要素不重复并且之间可以做差集运算，例如AddCity()方法中
        # self.AllowedCitySet = CitySet -
        # self.TabuCitySet，可以方便地从城市集合中去除禁忌城市列表的城市，获取允许的城市列表
        self.TabuCityList = []  # 定义禁忌城市空列表
        self.AllowedCitySet = set()  # 定义允许城市集合
        self.TransferProbabilityList = []  # 定义城市选择可能性列表
        self.CurrCity = 0  # 定义当前城市初始值为0
        self.CurrLen = 0.0  # 定义当前旅行路径长度
        # 执行AddCity()方法，获取每次迭代的当前城市CurrCity、禁忌城市列表TabuCityList和允许城市列表AllowedCitySet的值
        self.AddCity(currCity)

    def SelectNextCity(self, alpha, beta):  # 定义蚂蚁选择下一个城市的方法，需要参考前文描述的蚁群算法
        if len(self.AllowedCitySet) == 0:  # 如果允许城市集合为0，则返回0
            return (0)
        sumProbability = 0.0  # 定义概率，可能性初始值为0
        self.TransferProbabilityList = []  # 建立选择下一个城市可能性空列表
        for city in self.AllowedCitySet:  # 循环遍历允许城市集合
            sumProbability = sumProbability + (
                pow(self.pheromone_trail_list[self.CurrCity - 1][city - 1], alpha) *
                pow(1.0 / self.distance_matrix[self.CurrCity - 1][city - 1], beta)
            )
            # 蚂蚁选择下一个城市的可能性由信息素与城市间距离之间关系等综合因素确定，其中alpha为表征信息素重要程度的参数，beta为表征启发式因子重要程度的参数，
            # 该语句为前文蚁群算法阐述的选择下一个转移城市的概率公式的分母部分
            transferProbability = sumProbability  # 根据信息素选择公式和轮盘选择得出概率列表，非0-1
            self.TransferProbabilityList.append(
                (city, transferProbability))  # 将城市序号和对应的转移城市概率追加到转移概率列表中
#         print self.TransferProbabilityList
#         raw_input('prompt')
        threshold = sumProbability * random.random()  # 将概率值乘以一个0~1的随机数，获取轮盘指针值
        for (cityNum, cityProb) in self.TransferProbabilityList:  # 再次循环遍历概率列表
            if threshold <= cityProb:  # 如果轮盘指针值大于概率值，则返回对应的城市序号
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! key step!!!!!!!!!!!!!!!!
                return (cityNum)
        return (0)  # 否则返回0

#     #按照城市概率公式计算
#     def SelectNextCity(self, alpha, beta):  # 定义蚂蚁选择下一个城市的方法，需要参考前文描述的蚁群算法
#         if len(self.AllowedCitySet) == 0:  # 如果允许城市集合为0，则返回0
#             return (0)
#         Probability = 0.0
#         sumProbability = 0.0  # 定义概率，可能性初始值为0
#         self.TransferProbabilityList = []  # 建立选择下一个城市可能性空列表
#         for city in self.AllowedCitySet:  # 循环遍历允许城市集合
#             Probability = (
#                 pow(self.pheromone_trail_list[self.CurrCity - 1][city - 1], alpha) *
#                 pow(1.0 / CityDistanceList[self.CurrCity - 1][city - 1], beta)
#             )
#             sumProbability = sumProbability + Probability
#             self.TransferProbabilityList.append(
#                 [city,  Probability])  # 将城市序号和对应的转移城市概率追加到转移概率列表中
#         # 蚂蚁选择下一个城市的可能性由信息素与城市间距离之间关系等综合因素确定，其中alpha为表征信息素重要程度的参数，beta为表征启发式因子重要程度的参数，
#         # 该语句为前文蚁群算法阐述的选择下一个转移城市的概率公式的分母部分
#         for i in range(len(self.TransferProbabilityList)):
#             self.TransferProbabilityList[i][1] /= sumProbability
#         ProbabilityList = [x[1] for x in self.TransferProbabilityList]
#         maxProbability = max(ProbabilityList)
#         cityindex = ProbabilityList.index(maxProbability)
#         return (self.TransferProbabilityList[cityindex][0])

    def MoveToNextCity(self, alpha, beta):  # 定义转移城市方法
        # 执行SelectNextCity(),选择下一个城市的方法，获取选择城市的序号，并赋值给新的变量nextCity
        nextCity = self.SelectNextCity(alpha, beta)
        # 如果选择的城市序号大于0，则执行self.AddCity()方法，获取每次迭代的当前城市Currcity、禁忌城市列表TabuCityList和允许城市列表AllowedCitySet的值
        if nextCity > 0:
            self.AddCity(nextCity)  # 执行self.AddCity()方法

    def ClearTabu(self):  # 定义清楚禁忌城市方法，以用于下一次循环
        self.TabuCityList = []  # 初始化禁忌城市列表为空
        self.TabuCitySet.clear()  # 初始化城市禁忌列表为空
        self.AllowedCitySet = self.city_set - self.TabuCitySet  # 初始化允许城市集合

    def UpdatePathLen(self):  # 定义更新旅行路径长度方法
        for city in self.TabuCityList[0:-1]:  # 循环遍历禁忌城市列表
            nextCity = self.TabuCityList[
                self.TabuCityList.index(city) + 1]  # 获取禁忌城市列表中的下一个城市序号
            # 从城市间距离之中提取当前循环城市与下一个城市之间的距离，并逐次求和
            self.CurrLen = self.CurrLen + \
                self.distance_matrix[city - 1][nextCity - 1]
        lastCity = self.TabuCityList[-1]  # 提取禁忌列表中的最后一个城市
        firstCity = self.TabuCityList[0]  # 提取禁忌列表中的第一个城市
        # 将最后一个城市与第一个城市的距离值加到当前旅行路径长度，获取循环全部城市的路径长度
        self.CurrLen = self.CurrLen + \
            self.distance_matrix[lastCity - 1][firstCity - 1]

    def AddCity(self, city):  # 定义增加城市到禁忌城市列表中的方法
        if city <= 0:  # 如果城市序号小于等于0，则返回
            return
        self.CurrCity = city  # 更新当前城市序号
        self.TabuCityList.append(city)  # 将当前城市追加到禁忌城市列表中，因为已经旅行过的城市不应该再进入
        self.TabuCitySet.add(city)  # 将当前城市追加到禁忌城市集合中，用于差集运算
        self.AllowedCitySet = self.city_set - self.TabuCitySet  # 使用集合差集的方法获取允许的城市列表

    def two_opt_search(self):  # 领域搜索
        '''
        1-2-3-4, 1-2 + 3-4 > 1-3 + 2-4 则交换
        '''
#         print (self.TabuCityList) 
        cityNum = len(self.TabuCityList)
#         print (cityNum)
        for i in range(cityNum):
            for j in range(cityNum - 1, i, -1):
#                 print (i,j)
                curCity1 = self.TabuCityList[i] - 1
                preCity1 = self.TabuCityList[(i - 1) % cityNum] - 1
                curCity2 = self.TabuCityList[j] - 1
                nextCity2 = self.TabuCityList[(j + 1) % cityNum] - 1
#                 print (curCity1, preCity1 , curCity2, nextCity2)
                CurrLen = self.distance_matrix[preCity1][
                    curCity1] + self.distance_matrix[curCity2][nextCity2]
                NextLen = self.distance_matrix[preCity1][
                    curCity2] + self.distance_matrix[curCity1][nextCity2]
                if NextLen < CurrLen:
                    tempList = self.TabuCityList[i:j + 1]
                    self.TabuCityList[i:j + 1] = tempList[::-1]

def showResult(result, city_coordinate):
    x_coordination = []
    y_coordination = []
    # draw the result 
    for point in result:
        x_coordination.append(city_coordinate[point-1][0])
        y_coordination.append(city_coordinate[point-1][1])
    x_coordination.append(city_coordinate[result[0]-1][0]) # end to start
    y_coordination.append(city_coordinate[result[0]-1][1])

    plt.scatter(x_coordination,y_coordination)
    plt.plot(x_coordination,y_coordination)
    # draw the city mark
    for index in result:
        plt.text(city_coordinate[index-1][0], city_coordinate[index-1][1], index)  
    plt.text(city_coordinate[result[0]-1][0], city_coordinate[result[0]-1][1], '     Start')   #start   
    plt.text(city_coordinate[result[-1]-1][0], city_coordinate[result[-1]-1][1], '    End')   #end 
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The traveling map by ACO")
    plt.show()

if __name__ == '__main__':
    cost_matrix, city_list = Data.fromTSPFile("eil51.tsp")
    cost_matrix_list = cost_matrix.matrix
    # Create an initial solution
    number_of_cities = len(city_list)
    city_coordinate = []
    total_distance = 0
    for city in city_list:
        city_coordinate.append((city[1],city[2]))
    # change None to 0
    for i in range(len(cost_matrix_list)):
        cost_matrix_list[i][i] = 0
 
    city_id = [i for i in range(1, number_of_cities+1)]
    city_set = set(city_id)
    time_start = time.time()
    # solve the tsp by ACO
    theAntColony = AntColony(number_of_cities, city_set, cost_matrix_list, antCount=100, nMax = 10)  # AntColony class instance
    total_distance, city_result = theAntColony.Search()  
    time_end = time.time()
    print ('Time cost %s s.' % (time_end-time_start))
    print ('City solution:%s'% city_result)
    print ('The traveling total distance: %s' % total_distance) 
    showResult(city_result, city_coordinate)



 
# CityList = []  # 城市列表即存放代表城市的序号
# self.pheromone_trail_list = []  # 信息素列表（矩阵）
# self.pheromone_delta_trail_list = []  # 释放信息素列表（矩阵）
# CityDistanceList = []  # 两两城市距离列表(矩阵)
# AntList = []  # 蚂蚁列表

# #     theAntColony.initCity()  # read the city data
#     
#     time_end = time.time()
#     print ('Time cost %s s.' % (time_end-time_start))
#     print ('City solution:%s'% city_solution)
#     theAntColony = AntColony(cityCount=51, antCount=100, nMax = 100)  # AntColony class instance
# #     theAntColony.initCity()  # read the city data
#     
