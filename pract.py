import networkx as nx
import matplotlib.pyplot as plt
import random
import queue
import sampling
import concept


def present(g, sub, col=['#dbb844'],pos=None):
    #takes graph, list of sub node lists, and list of colors
    if pos==None:
        pos=nx.spring_layout(g)
    dcol='#668aae'
    nL=[x for x in g.nodes() if not x in sub]
    cL=[dcol]*len(nL)
    for i in range(0,len(sub)):
        nL.extend(sub[i])
        cL.extend([col[i]]*len(sub[i]))
    nx.draw(g, nodelist=nL, node_color=cL, with_labels=False, pos=pos)
    plt.show()

def readG(f):
    f=open(f, 'rb')
    G=nx.read_edgelist(f)#, nodetype='int')#, delimiter='\n')
    f.close()
    return G

def prop(g):
    Active=set()
    #pos=nx.spring_layout(g)
    while target.newNodes:
        newActive=target.newNodes
        print(newActive)
        #present(g, [target.active],['#dd4f5f'], pos=pos)
        target.update()

#G=readG('gr.txt')
#sG=G.subgraph(sn)
#target=concept.Concept(G, name='target', seedsize=8, factor=0.2)
#prop(G)
