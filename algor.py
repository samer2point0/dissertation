import networkx as nx
import random
import copy
import queue
import sampling
import time

#import pres

def randseed(g, p, seedsize, tSet=None, r=1):
    nodes=list(g.nodes)
    seed= set(random.choices(nodes,k=seedsize))
    while len(seed)<seedsize:
        seed.add(random.choice(nodes))
    return seed

def randApart(g, p, seedsize, tSet=None, r=1):
    ln=list(g.nodes)
    D=dict(g.degree)
    topD=list(sorted(D, key=lambda x: D[x], reverse=False))
    seed=set()
    EI=int(seedsize*p*g.size()/g.number_of_nodes())
    while True:
        max=topD.pop()
        pr=D[max]/g.size()
        prob=EI*pr*pow((1-pr),(EI-1))
        if prob < 0.2:
            break


    while len(seed)<seedsize:
        sel=random.choice(ln)
        if not sel in seed and sel in topD:
            seed.add(sel)
    return seed

def degree(g,p, seedsize, tSet=None, r=1):
    ln=list(g.nodes)
    D=dict(g.degree)
    topD=list(sorted(D, key=lambda x: D[x], reverse=False))
    seed=set()
    EI=int(seedsize*p*g.size()/g.number_of_nodes())
    while True:
        max=topD.pop()
        pr=D[max]/g.size()
        prob=EI*pr*pow((1-pr),(EI-1))
        if prob < 0.2:
            break

    seed=set(topD[-seedsize:-1])
    return seed


def sinDisc(g,p,  seedsize, tSet=None, r=1):#minus tSet
    l=dict(g.degree)
    seed=set()

    while True:
        v=max(l, key=lambda x:l[x])
        if not v in tSet:
            seed.add(v)
        if len(seed)==seedsize:
            break
        neigh=list(g.neighbors(v))
        for pot in neigh:
            if not pot in seed and not pot in tSet:
                l[pot]=l[pot]-1

        del l[v]
    return seed

def degDisc(g,p, seedsize, tSet=None, r=1):#minus tSet
    l=dict(g.degree)
    seed=set()


    while True:
        v=max(l, key=lambda x:l[x])
        if not v in tSet:
            seed.add(v)
        if len(seed)==seedsize:
            break

        neigh=set(g.neighbors(v))
        for u in neigh:
            nei=set(g.neighbors(u))
            tu=len(neigh.intersection(seed))
            if not u in seed and not u in tSet:
                l[u]=l[u]-2*tu-(l[u]-tu)*p*tu

        del l[v]
    return seed


def MPG(g,p, seedsize, tSet=None, r=1):
    #begin=time.time()
    thresh=0.001
    N=dict()
    seed=set()
    neigh=set()
    i=1
    Set=tSet
    while pow(p,i)>thresh:
        for t in Set:#equal wieghts and propagation probal <0.1
            nei=[x for x in g.neighbors(t) if not(x in tSet)]#only works if i<=2 (must delete node resulting in it's influence)
            neigh=neigh.union(set(nei))
            for n in nei:
                if not n in N.keys():
                    N[n]={'aProb':0, 'expGain':0, 'weGain':0, 'parents':set()}

                N[n]['aProb']=N[n]['aProb']+p
                if not i==1:
                    N[n]['parents'].add(t)
        Set=neigh.difference(Set)
        i=i+1

    for n in neigh:
        N[n]['expGain']=g.degree[n]*p #equal weights
        N[n]['weGain']=N[n]['aProb']*N[n]['expGain']

    while True:
        v=max(N, key=lambda x:N[x]['weGain'])
        if not (v in tSet):
            seed.add(v)
        if len(seed)==seedsize:
            break

        #update expected gain
        for pa in N[v]['parents']:
            if not pa in seed and not pa in tSet:
                N[pa]['expGain']=N[pa]['expGain']-p+r*p
                N[pa]['weGain']=N[pa]['aProb']*N[pa]['expGain']

        #update activation prob
        nei=neigh.intersection(g.neighbors(v))
        for k in nei:
            if not k in seed and not k in tSet:
                N[k]['aProb']=N[k]['aProb']-p+p*r
                N[k]['weGain']=N[k]['aProb']*N[k]['expGain']

        del N[v]
    #print(time.time()-begin)
    return seed


def degN(g,p, seedsize, tSet=None, r=1):
    neigh=copy.deepcopy(tSet)
    l=dict(g.degree)
    D={}
    c=0.9
    Set=[tSet]

    for i in range(0,3):
        nei=set()
        for t in Set[i]:
            nei=nei.union(set(g.neighbors(t)))
        nei=nei.difference(neigh)
        Set.append(nei)
        neigh=neigh.union(nei)

    neigh=neigh.difference(tSet)

    topD=list(sorted(l, key=lambda x: l[x], reverse=False))
    EI=int(seedsize*p*g.size()/g.number_of_nodes())
    while True:
        m=topD.pop()
        pr=l[m]/g.size()
        prob=EI*pr*pow((1-pr),(EI-1))
        if prob < 0.2:
            break
        elif m in neigh:
            neigh.remove(m)

    for i in range(1,4):
        for n in Set[i]:
            l[n]=l[n]*pow(c,i-1)

    seed=set()
    temp=set()
    while True:
        v=max(l, key=lambda x:l[x])
        temp.add(v)
        if v in neigh:
            seed.add(v)
            if len(seed)==seedsize:
                break
            nei=[x for x in g.neighbors(v) if not x in temp]
            for pot in nei:
                l[pot]=l[pot]-1

        del l[v]
    return seed


def voteN(g,p, seedsize, tSet=None, r=1):
    #begin=time.time()
    ln=list(g.nodes)
    avgd=g.size()/g.number_of_nodes()
    Q=copy.deepcopy(tSet)
    seed=set()
    V=dict(zip(ln,[0]*len(ln)))
    VP=dict(zip(ln,[1]*len(ln)))
    k=int(seedsize/10)
    c=nx.average_clustering(g,tSet)
    while True:
        q=copy.deepcopy(Q)
        for n in q:
            Q.remove(n)
            nei=[x for x in g.neighbors(n) if not x in seed and not x in tSet]
            random.shuffle(nei)
            i=0
            for vote in nei:
                V[vote]=V[vote]+VP[n]
                if i<=2 and VP[vote]>0:
                    Q.add(vote)
                    i=i+1

        for j in range(k):
            topk=max(V, key=lambda x: V[x]  if not x in tSet else 0)
            seed.add(topk)
            if(len(seed)==seedsize):
                break
            if topk in Q:
                Q.remove(topk)
            del V[topk]
            nei=[x for x in g.neighbors(topk) if not x in seed and not x in tSet]
            for n in nei:
                VP[n]=max(0, VP[n]-c)

        if(len(seed)==seedsize):
            break
    #print(time.time()-begin)
    return seed

def close(g,p, seedsize, tSet=None, r=1):
    l=dict(g.degree)
    tpot=list(sorted(l, key=lambda x: l[x], reverse=True))[0:int(seedsize*2)]
    pot=set(tpot)
    CD=dict(zip(pot,[0]*len(pot)))
    flag=set()
    sw=5

    for t in tSet:
        Set=set(g.neighbors(t))
        for n in Set:
            if ((n in pot) and (not (t,n) in flag)):
                flag.add((t,n))
                CD[n]=CD[n]+1

            Set1=set([x for x in g.neighbors(n) if x not in Set])
            for n1 in Set1:
                if ((n1 in pot) and (not (t,n1) in flag)):
                    flag.add((t,n1))
                    CD[n1]=CD[n1]+2

        leftpot=[x for x in pot if not (t,x) in flag]
        for p in leftpot:
            flag.add((t,p))
            CD[p]=CD[p]+sw

    seed=set(sorted(CD, key=lambda x: CD[x], reverse=False)[0:seedsize])

    return seed

def noSeed(g,p, seedsize, tSet=None, r=1):
    return set()
