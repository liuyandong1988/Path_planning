from matplotlib import pyplot as plt
#-----------------------------------------------------------------------------
def showResult(result, city_coordination, city_num):
    color = ['red', 'yellow', 'blue', 'green','orange']
    style = ['o', 'p', 's', '*', '^']
    x_coordination = []
    y_coordination = []
    x_coordination_each = []
    y_coordination_each = []
    plt.figure(1)
    for vehicle, path in result.items():
        x_coordination_each = []
        y_coordination_each = []
        # draw the result 
        for point in path:
            x_coordination_each.append(city_coordination[point-1][0])
            y_coordination_each.append(city_coordination[point-1][1])
        x_coordination.append(x_coordination_each)
        y_coordination.append(y_coordination_each)
        plt.scatter(x_coordination[vehicle-1],y_coordination[vehicle-1], c =color[vehicle-1], marker = style[vehicle-1])
        plt.plot(x_coordination[vehicle-1],y_coordination[vehicle-1])
    for index in range(city_num):
        plt.text(city_coordination[index][0], city_coordination[index][1], index+1)  
    plt.xlabel('City x coordination')
    plt.ylabel("City y coordination")
    plt.title("The VRP map by ***")
    plt.grid()
    plt.show()  