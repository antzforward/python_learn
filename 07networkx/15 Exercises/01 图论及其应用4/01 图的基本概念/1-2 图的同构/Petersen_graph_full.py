import networkx as nx
import inspect
import matplotlib.pyplot as plt
from networkx.drawing import layout
'''
之前使用所有的layout，然后用默认值的时候，发现经典的Petersen图都没有布局出来
这里换个思路，就是直接写出所有的layout，根据不同的表现形式，可以会同一个layout
有不同参数，反正就是列出尽可能多的表现形式，然后给每个设定个名字。
因为书上的题目中设计的Petersen图我都没显示出来。
'''

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 创建Petersen graph
G = nx.petersen_graph()

# 设置经典Petersen图布局，外五边形+内五角星，手动布置，五个在外