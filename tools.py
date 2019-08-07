import networkx as nx
import sampling
import concept
import algor
import numpy
import copy
import pandas as pd
import itertools
import random


def readG(fname):
    f=open('./samples/'+fname+'.txt', 'rb')
    G=nx.read_edgelist(f)#, nodetype='int')#, delimiter='\n')
    g= G.subgraph(max(list(nx.connected_components(G)), key=lambda x:len(x)))
    f.close()
    return g

def saveRes(gType, l, kw):
    #organized by graoh
    #must save differently for each sample
    try:
        DF=pd.read_csv('./tests/'+gType+'_test.txt')
    except IOError:
        DF=pd.DataFrame()#index=[list(kw.values())]))#columns=list(range(0,len(l))))


    exp=str(list(kw.values()))
    df=pd.DataFrame(l,columns=[exp])
    if exp in DF.columns:
        ax=0
    else:
        ax=1
    DF=pd.concat([df,DF], axis=ax, join='outer')
    print(DF)
    DF.to_csv('./tests/'+gType+'_test.txt', index=False)

def prop(g):
    print('number of nodes', g.number_of_nodes())
    print('no of edges ', g.size())
    print('graph has ', nx.number_connected_components(g), 'connected component')
