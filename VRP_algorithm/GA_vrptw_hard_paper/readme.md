使用《A New Genetic Algorithm For VRPTW》中的GA算法



- 求解Solomon数据集，硬vrptw问题。
- 使用Nearest Neighbor 贪婪算法，随机序列方法初始化种群。
- 依赖时间窗约束、返回depot约束和车辆负载约束解码染色体，得到一组可行解，并计算车辆的行驶距离。
- 下一代种群：
	- selection：随机采样2个个体，90%选择适应度大的个体，10%选择使用适应度小的。
	- crossover：分distance最近和start time最近做交叉
	- mutation：2种变异方式，（1）颠倒顺序（2）交换两个基因
- 形成符合种群数量的子代个体

- 
- 