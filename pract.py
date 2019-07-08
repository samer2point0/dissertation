import networkx as nx
import matplotlib.pyplot as plt
import random
import queue
import sampling as smp
import concept

def prop():
    while target.newNodes:
        target.update()
        print(sG.nodes)
f=open('gr.txt', 'rb')
G=nx.read_edgelist(f)#, nodetype='int')#, delimiter='\n')
f.close()
sn=smp.mhda(G)
sG=G.subgraph(sn)
#print(sG.nodes)
#nx.draw(sG, with_labels=True)
#plt.show()

target=concept.Concept(sG, name='target')
prop()

"""
sn=smp.snowball(G)
sG=G.subgraph(sn)
print(sG.nodes)
nx.draw(sG, with_labels=True)
plt.show()
"""
