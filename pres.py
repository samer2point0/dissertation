import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import algor
import itertools
import copy

def drawN(g, sub, col=['#dbb844'],pos=None):
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

flist=['MPG', 'randseed', 'degree', 'neisinD', 'degDisc', 'sinDisc']
fflist=itertools.product(flist, repeat=2)
DF=pd.read_csv('astroph_test.txt')
#print(list(fflist))
matrix(DF, fflist)
