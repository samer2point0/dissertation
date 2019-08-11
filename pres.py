import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import itertools
import copy
import sampling
import random


FuncList=['noSeed', 'randseed', 'degree','sinDisc', 'degDisc', 'MPG', 'close', 'degN', 'voteN']
SetupList=[[0.02,0.05], [[2,0.5], [5,0.2]], [100, 250,500]]

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

def matrix(gName, flist=FuncList, slist=SetupList):
    DF=pd.read_csv('./tests/'+gName+'_test.txt')
    fflist=list(itertools.product(flist, repeat=2))
    sslist=list(itertools.product(*slist))
    for s in sslist:
        m=pd.DataFrame(numpy.zeros((len(flist),len(flist))), columns=flist, index=flist)
        std=pd.DataFrame(numpy.zeros((len(flist),len(flist))), columns=flist, index=flist)
        for ffpair in fflist:
            c=str([ffpair[0], ffpair[1], s[0], s[1], s[2]])
            if c in DF.columns:
                #col boost and rows inH
                m[ffpair[0]].loc[ffpair[1]]=DF[c].mean()
                std[ffpair[0]].loc[ffpair[1]]=DF[c].std()

        print('\n\nBellow are the mean and std matrix for the set up \n',c)
        print(m,'\n\n', std)
