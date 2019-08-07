import networkx as nx
import sampling
import concept
import algor
import numpy
import copy
import pandas as pd
import itertools
import random
import pres

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

def test(gType, save=False, FB=algor.randseed, FinH=algor.randseed, PP=0.05, r=[2,0.5], seedsize=250):
    l=[]
    for i in range(0,100):
        if 'smp' in gType:  #if network should be sampled
            n=random.choice(range(50))
            g=readG(gType+str(n)) #ex: dplb_snow_smp10
        elif i==0: #if not only read netwokr in first run
            g=readG(gType)

        T=concept.Concept(g, 'target', PP=PP, r=r, seedsize=seedsize)
        tSet=copy.deepcopy(T.seed)
        B=concept.Concept(g, 'B', func=FB, PP=PP, r=r, seedsize=seedsize, tSet=tSet)
        inH=concept.Concept(g, 'inH', func=FinH, PP=PP, r=r, seedsize=seedsize, tSet=tSet)

        seed=random.choice(list(tSet))
        sample1=sampling.mhda(g, seed=seed, maxsize=50)
        sample2=sampling.snow(g, seed=seed, maxsize=100)
        pos1, pos2=None, None
        while T.newNodes:
            #pos1=pres.drawNsmp(g, sample1, copy.deepcopy([T.active, B.active, T.active.intersection(B.active),set([seed])]), size=200, col=['yellow', '#668aae', 'green', 'red'], pos=pos1)
            #pos2=pres.drawNsmp(g, sample2, copy.deepcopy([T.active, B.active,T.active.intersection(B.active),set([seed])]), size=200, col=['yellow', '#668aae', 'green', 'red'], pos=pos2)
            T.update()
            B.update()
            inH.update()
        l.append(len(T.active))
        #print(l[i])

    l=numpy.array(l)

    if save:
        kw={'FB':FB.__name__, 'FinH':FinH.__name__, 'PP':PP, 'r':r, 'seedsize':seedsize}
        saveRes(gType, l, kw)
    else:
        print('target has spread to ', numpy.average(l), ' nodes with a std dev of ', numpy.std(l))

def tfunc(graph, flist=[algor.MPG, algor.randseed, algor.degree, algor.degDisc, algor.sinDisc, algor.close, algor.voteN, algor.degN]):
    fflist=itertools.product(flist, repeat=2)
    #(PP,r,seedsize)
    setup=itertools.product([0.02,0.05], [[2,0.5], [5,0.2]], [250,500])
    for ff in fflist:
        for s in setup:
            test(graph, save=True, FB=ff[0], FinH=ff[1])
            break
            #doesn't run
            test(graph, save=True, FB=ff[0], FinH=ff[1], PP=s[0], r=s[1], seedsize=s[2])

def prop(g):
    print('number of nodes', g.number_of_nodes())
    print('no of edges ', g.size())
    print('graph has ', nx.number_connected_components(g), 'connected component')

#g=readG('astroph.txt')
#test('astroph', save=False, PP=0.05, FB=algor.MPG, seedsize=250)
#test('gr', save=False, PP=0.05, FB=algor.close, seedsize=250)
tfunc('astroph')
#prop(g)
