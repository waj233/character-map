import networkx as nx
import matplotlib.pyplot as plt

import jieba
import codecs
import jieba.posseg as pseg





#分词得到人物节点
with codecs.open("剧情梗概.txt", "r") as f:
    for line in f.readlines():
        poss = pseg.cut(line)       # 分词并返回该词词性
        lineNames = []
        lineNames.append([])        # 为新读入的一段添加人物名称列表
        for w in poss:
            if w.flag != "nr" or len(w.word) < 2:
                continue
            lineNames[-1].append(w.word)# 为当前段的环境增加一个人物
            names = {}
            relationships = {}
            if names.get(w.word) is None:
                names[w.word] = 0
                relationships[w.word] = {}
            names[w.word] += 1                  # 该人物出现次数加 1


for line in lineNames:
    for name1 in line:
        for name2 in line:
            if name1 == name2:
                continue
            if relationships[name1].get(name2) is None:     # 若两人尚未同时出现则新建项
                relationships[name1][name2]= 1
            else:
                relationships[name1][name2] = relationships[name1][name2]+ 1        # 两人共同出现次数加 1

#保存文件
with codecs.open("renwu.txt", "a+", "utf-8") as f:
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 20:
                f.write(name + " " + v + " " + str(w) + "\r\n")

#读取文件
a = []
f = open('renwu.txt','r',encoding='utf-8')
line = f.readline()
while line:
    a.append(line.split())
    line = f.readline()
f.close()

#绘图
G = nx.Graph()
G.add_weighted_edges_from(a)
nx.draw(G,with_labels=True,font_size=12,node_size=1000,node_color='g')
plt.show()
