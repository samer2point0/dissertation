import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import algor
import itertools
import copy
import sampling
import random

def drawN(g, sub, col=['#dbb844'],pos=None):
    #takes graph, list of sub node lists, and list of colors
    if pos==None:
        pos=nx.spring_layout(g)
    dcol='black'
    nL=list(g.nodes())
    cL=[dcol]*len(nL)
    for i in range(0,len(sub)):
        nL.extend(sub[i])
        cL.extend([col[i]]*len(sub[i]))

    nx.draw(g, nodelist=nL, node_color=cL, with_labels=False, pos=pos, node_size=20, width=0.1)
    plt.show()
    return pos

def drawNsmp(g, sample, sub, size=100, col=None, pos=None):#graogh, set or list, list of sets, ..
    G=g.subgraph(sample)
    for i in range(0,len(sub)):
        sub[i]=list(sub[i].intersection(sample))

    pos=drawN(G, sub, col=col, pos=pos)
    return pos

def matrix(DF, exL):
    exl=copy.deepcopy(exL)
    L=set(list(zip(*exl))[0])
    m=pd.DataFrame(numpy.zeros((len(L),len(L))), columns=L, index=L)
    s=pd.DataFrame(numpy.zeros((len(L),len(L))), columns=L, index=L)
    for exp in exL:
        #only loops through functions now
        c=str([exp[0], exp[1], 0.05, [2, 0.5], 250])
        if c in DF.columns:
            #col boost and rows inH
            m[exp[0]].loc[exp[1]]=DF[c].mean()
            s[exp[0]].loc[exp[1]]=DF[c].std()

    print(m,'\n\n', s)

"""
flist=['MPG', 'randseed', 'degree', 'neisinD', 'degDisc', 'sinDisc']
fflist=itertools.product(flist, repeat=2)
DF=pd.read_csv('gr_test.txt')
#print(list(fflist))
matrix(DF, fflist)
"""
