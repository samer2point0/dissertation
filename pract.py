import networkx as nx
import matplotlib.pyplot as plt
import random
import queue
import sampling
import concept
import algor
import numpy
import copy

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
    g=nx.read_edgelist(f)#, nodetype='int')#, delimiter='\n')
    f.close()
    return g

def test(g, FB=algor.randseed, FinH=algor.randseed, PP=0.05, r=[2,0.5], seedsize=100):
    #pos=nx.spring_layout(g)
    l=[]
    for i in range(0,100):
        G=copy.deepcopy(g)
        T=concept.Concept(G, 'target', PP=PP, r=r, seedsize=seedsize)
        tSet=copy.deepcopy(T.seed)
        B=concept.Concept(G, 'B', func=FB, PP=PP, r=r, seedsize=seedsize, tSet=tSet)
        inH=concept.Concept(G, 'inH', func=FinH, PP=PP, r=r, seedsize=seedsize, tSet=tSet)
        while T.newNodes:
            T.update()
            B.update()
            inH.update()
        l.append(len(T.active))

    l=numpy.array(l)
    print('target has spread to ', numpy.average(l), ' nodes with a std dev of ', numpy.std(l))


G=readG('gr.txt')
test(G, PP=0.05,FB=algor.MPG, seedsize=250)
test(G, PP=0.05,FB=algor.degree, seedsize=250)
