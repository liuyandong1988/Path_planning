from math import *
import random
CityList = []
CitySet = []
CityDistanceList = []
CityCount = 0

#calculate the random initial

def initCity():
    """Get the city data"""
    f=open("elit51.txt","r")
    while True:
        #read the city data
        loci = str(f.readline())
        if loci:
            pass  # do something here
        else:
            break
        loci = loci.replace("\n", "")
        loci=loci.split()
        #index coordination_x coordination_y
        CityList.append((int(loci[0]),float(loci[1]),float(loci[2])))
        CitySet.append(int(loci[0]))
        CityCount = len(CityList)
    for row in range(CityCount):  # city number
        distanceList = []  # distance between cities
        for col in range(CityCount):
            distance = sqrt(pow(CityList[row][1] - CityList[col][1], 2) + pow(
                CityList[row][2] - CityList[col][2], 2)) 
            distance = round(distance)
            distanceList.append(distance) 
        CityDistanceList.append(distanceList)
#     print CityDistanceList

initCity()   
random.shuffle(CitySet)

CitySet = [13, 42, 43, 3, 9, 37, 41, 17, 10, 15, 45, 19, 4, 6, 48, 47, 31, 27, 2, 51, 11, 8, 36, 26, 32, 29, 20, 35, 39, 30, 34, 49, 50, 44, 25, 33, 16, 12, 14, 24, 46, 28, 22, 5, 40, 7, 21, 23, 38, 1, 18]
result = 0
for city in CitySet[0:-1]:
    result += CityDistanceList[city-1][CitySet[CitySet.index(city)+1]-1]
result += CityDistanceList[CitySet[-1]-1][CitySet[0]-1]
print result