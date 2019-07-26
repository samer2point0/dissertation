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
    g=nx.read_edgelist(f)#, nodetype='int')#, delimiter='\n')
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

    if save:
        kw={'FB':FB.__name__, 'FinH':FinH.__name__, 'PP':PP, 'r':r, 'seedsize':seedsize}
        saveRes(gType, l, kw)
    else:
        print('target has spread to ', numpy.average(l), ' nodes with a std dev of ', numpy.std(l))

def tfunc(flist=[algor.MPG, algor.randseed, algor.degree, algor.myDisc, algor.degDisc, algor.sinDisc]):
    fflist=itertools.product(flist, repeat=2)
    for ff in fflist:
        test('gr', save=True, PP=0.05, FB=ff[0], FinH=ff[1], seedsize=250)

test('gr', save=True, PP=0.05, FB=algor.randseed, FinH=algor.degC, seedsize=250)
