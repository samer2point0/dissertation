import networkx as nx
import sampling
import concept
import algor
import numpy
import copy
import pandas as pd
import itertools

def readG(f):
    f=open(f, 'rb')
    G=nx.read_edgelist(f)#, nodetype='int')#, delimiter='\n')
    g= G.subgraph(max(list(nx.connected_components(G)), key=lambda x:len(x)))
    f.close()
    return g

def saveRes(gType, l, kw):
    #organized by graoh
    #must save differently for each sample
    try:
        DF=pd.read_csv(gType+'_test.txt')
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
    DF.to_csv(gType+'_test.txt', index=False)

def test(gType, save=False, FB=algor.randseed, FinH=algor.randseed, PP=0.05, r=[2,0.5], seedsize=100):
    l=[]
    g=readG(gType+'.txt')
    for i in range(0,10):
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
        print(l[i])

    l=numpy.array(l)

    if save:
        kw={'FB':FB.__name__, 'FinH':FinH.__name__, 'PP':PP, 'r':r, 'seedsize':seedsize}
        saveRes(gType, l, kw)
    else:
        print('target has spread to ', numpy.average(l), ' nodes with a std dev of ', numpy.std(l))

def tfunc(graph, flist=[algor.MPG, algor.randseed, algor.degree, algor.degDisc, algor.sinDisc, algor.close]):
    fflist=itertools.product(flist, repeat=2)
    for ff in fflist:
        test(graph, save=True, PP=0.05, FB=ff[0], FinH=ff[1], seedsize=250)

def prop(g):
    print('number of nodes', g.number_of_nodes())
    print('no of edges ', g.size())
    print('graph has ', nx.number_connected_components(g), 'connected component')

#g=readG('astroph.txt')
#test('gr', save=False, PP=0.05, FB=algor.sinDisc, seedsize=250)
test('gr', save=False, PP=0.05, FB=algor.voteN, seedsize=250)
#tfunc('astroph')
#prop(g)
