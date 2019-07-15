import networkx as nx
import matplotlib.pyplot as plt
import random
import queue
import sampling as smp
import concept


def prop(g):
    Active=set()
    while target.newNodes:
        newActive=target.newNodes
        Active=Active.union(newActive)
        print(newActive)
        target.update()




f=open('gr.txt', 'rb')
G=nx.read_edgelist(f)#, nodetype='int')#, delimiter='\n')
f.close()
sn=smp.mhda(G)
sG=G.subgraph(sn)
#print(sG.nodes)
#nx.draw(sG, with_labels=True)
#plt.show()

target=concept.Concept(sG, name='target')
prop(sG)
