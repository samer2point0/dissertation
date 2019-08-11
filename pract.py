import networkx as nx
import sampling
import concept
import algor
import numpy
import copy
import itertools
import random
import pres
import tools


FuncList=[algor.MPG, algor.randseed, algor.degree, algor.degDisc, algor.sinDisc, algor.close, algor.voteN, algor.degN, algor.noSeed, algor.randApart]
SetupList=[[0.02, 0.05], [[2,0.5], [5,0.2]], [100, 250,500]]

def test(gName, save=False, FB=algor.randseed, FinH=algor.randseed, PP=0.05, r=[2,0.5], seedsize=250):
    l=[]
    kw={'FB':FB.__name__, 'FinH':FinH.__name__, 'PP':PP, 'r':r, 'seedsize':seedsize}
    for i in range(0,10):
        if save and tools.expinDF(gName, kw):
            break #break if expirement already saved
        if 'smp' in gName:  #if network should be sampled
            n=random.choice(range(50))
            g=tools.readG(gName+str(n)) #ex: dplb_snow_smp10
        elif i==0: #if not only read netwokr in first run
            g=tools.readG(gName)

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
        tools.saveRes(gName, l, kw)
    else:
        print('target has spread to ', numpy.average(l), ' nodes with a std dev of ', numpy.std(l))

def tfunc(graph, flist=FuncList, slist=SetupList):
    fflist=list(itertools.product(flist, repeat=2))
    setup=list(itertools.product(*slist)) #(PP,r,seedsize)
    for s in setup:
        for ffpair in fflist:
            #test(graph, save=True, FB=ff[0], FinH=ff[1])
            #break
            #doesn't run
            test(graph, save=True, FB=ffpair[0], FinH=ffpair[1], PP=s[0], r=s[1], seedsize=s[2])

def replaceEXP(gName, L):
    expList=itertools.product(L[0],L[1],L[2],L[3],L[4])
    for l in expList:
        tools.delExp([l[0].__name__, l[1].__name__, l[2],l[3],l[4]], gName)
        test(gName, save=True, FB=l[0], FinH=l[1], PP=l[2], r=l[3], seedsize=l[4])
        pres.matrix(gName, slist=[[l[2]],[l[3]], [l[4]]])

def replaceAT(gName, a):
    expList=tools.delAtr(gName, a)
    sL=[x.__name__ for x in FuncList]
    for l in expList:
        l[0]=FuncList[sL.index(l[0])]
        l[1]=FuncList[sL.index(l[1])]
        test(gName, save=True, FB=l[0], FinH=l[1], PP=l[2], r=l[3], seedsize=l[4])
        #pres.matrix(gName, slist=[[l[2]],[l[3]], [l[4]]])

#tfunc('gr')
#pres.matrix('gr')

#replaceEXP('gr', [[algor.randApart], [algor.noSeed], [0.05], [[5,0.2]], [500]])

#VS
test('astroph', FB=algor.voteN, FinH=algor.noSeed,PP=0.05, r=[5,0.2], seedsize=500)
#test('astroph', FB=algor.degDisc, FinH=algor.degN,PP=0.05, r=[5,0.2], seedsize=250)
