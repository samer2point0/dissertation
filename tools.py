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


def saveRes(gName, l, kw):
    #organized by graoh
    #must save differently for each sample
    try:
        DF=pd.read_csv('./tests/'+gName+'_test.txt')
    except IOError:
        DF=pd.DataFrame()#index=[list(kw.values())]))#columns=list(range(0,len(l))))


    exp=str(list(kw.values()))
    df=pd.DataFrame(l,columns=[exp])
    if not exp in DF.columns:
        DF=pd.concat([df,DF], axis=1, join='outer')
        print(DF)
        DF.to_csv('./tests/'+gName+'_test.txt', index=False)

def expinDF(gName, kw):
    try:
        DF=pd.read_csv('./tests/'+gName+'_test.txt')
    except IOError:
        DF=pd.DataFrame()#index=[list(kw.values())]))#columns=list(range(0,len(l))))

    exp=str(list(kw.values()))
    if exp in DF.columns:
        return True
    else:
        return False

def delF(gName, f):
    DF=pd.read_csv('./tests/'+gName+'_test.txt')
    L=[]
    for exp in DF.columns:
        if f in exp:
            L.append(eval(exp))
            DF.drop(columns=exp, inplace=True)
    DF.dropna(axis=0, how='all', inplace=True)
    DF.to_csv('./tests/'+gName+'_test.txt', index=False)
    print(DF)
    return L


def nsample(gName, n, sampler, size=20000):
    g=readG(gName)
    for i in range(n):
        path='./samples/'+gName+'_'+sampler.__name__+'_smp'+str(i)+'.txt'
        sn=sampler(g, maxsize=size)
        sG=g.subgraph(sn)
        nx.write_edgelist(sG, path)
        print(path)

def prop(g):
    print('number of nodes', g.number_of_nodes())
    print('no of edges ', g.size())
    print('graph has ', nx.number_connected_components(g), 'connected component')

def delExp(l, gName):
    DF=pd.read_csv('./tests/'+gName+'_test.txt')
    exp=str(l)
    if exp in DF.columns:
        DF.drop(columns=exp, inplace=True)
    DF.dropna(axis=0, how='all', inplace=True)
    DF.to_csv('./tests/'+gName+'_test.txt', index=False)
    print(DF)

def merge(gName, ax=0):
    DF1=pd.read_csv('./tests/'+gName+'_test1.txt')
    DF2=pd.read_csv('./tests/'+gName+'_test2.txt')
    DF=pd.concat([DF1,DF2], axis=0, join='outer')
    print(DF1.shape, DF2.shape, DF.shape)
    DF.to_csv('./tests/'+gName+'_test.txt', index=False)
