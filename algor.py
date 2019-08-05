import networkx as nx
import random
import copy
import heapq
import sampling
import tools

def randseed(g, p, seedsize, tSet=None, r=1):
    return set(random.choices(list(g.nodes),k=seedsize))

def degree(g,p, seedsize, tSet=None, r=1):
    l=sorted(g.degree, key=lambda x: x[1], reverse=True)
    return set([x[0] for x in l[0:seedsize]])


def myDisc(g,p,  seedsize, tSet=None, r=1):
    l=sorted(g.degree, key=lambda x: x[1])
    seed=[l.pop()[0]]
    neigh=list(g.neighbors(seed[0]))
    pot=[l.pop()]
    if pot in neigh:
        pot[0][1]=pot[0][1]-1
    flag=1
    while flag:
        x=l.pop()
        while (not pot==[]) and x[1]<pot[-1][1]:
            seed.insert(0, pot.pop()[0])
            neigh.extend(list(g.neighbors(seed[0])))

        if len(seed)>=seedsize:
            flag=0
            break

        x=(x[0],x[1]-neigh.count(x[0])) #discount 1 for each edge alfeady in set
        i=0
        while True:
            if i==len(pot):
                pot.insert(-1,x)
                break
            if x[1]<pot[i][1]:
                pot.insert(i,x)
                break
            i=i+1
    return set(seed[0:seedsize])

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
                    N[n]={'ap':0, 'eg':0, 'we':0, 'parents':set()}

                N[n]['ap']=N[n]['ap']+p
                if not i==1:
                    N[n]['parents'].add(t)
        Set=neigh.difference(Set)
        i=i+1

    for n in neigh:
        N[n]['eg']=g.degree[n]*p #equal weights
        N[n]['we']=N[n]['ap']*N[n]['eg']


    while True:
        v=max(N, key=lambda x:N[x]['we'])
        if not (v in tSet):
            seed.add(v)
        if len(seed)==seedsize:
            break

        #update expected gain
        for pa in N[v]['parents']:
            if not pa in seed and not pa in tSet:
                N[pa]['eg']=N[pa]['eg']-p+r*p
                N[pa]['we']=N[pa]['ap']*N[pa]['eg']

        #update activation prob
        nei=neigh.intersection(g.neighbors(v))
        for k in nei:
            if not k in seed and not k in tSet:
                N[k]['ap']=N[k]['ap']-p+p*r
                N[k]['we']=N[k]['ap']*N[k]['eg']

        del N[v]
    return seed


def degN(g,p, seedsize, tSet=None, r=1):
    neigh=set()
    l=dict(g.degree)
    D={}
    c=0.9
    Set=[tSet]
    for i in range(0,3):
        nei=set()
        for t in Set[i]:
            nei=nei.union(set(g.neighbors(t)))
        Set.append(nei)
        neigh=neigh.union(nei)

    neigh=neigh.difference(tSet)

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
            nei=list(g.neighbors(v))
            for pot in nei:
                if not pot in temp:
                    l[pot]=l[pot]-1

        del l[v]
    return seed

def betC(g,p, seedsize, tSet=None, r=1):
    #487mean, 41std

    C=nx.betweenness_centrality_subset(g, tSet, tSet)
    seed=set(sorted(C, key=lambda x: C[x] if not (x in tSet) else 0, reverse=True)[0:seedsize])
    return seed

def NbetC(g,p, seedsize, tSet=None, r=1):
    neigh=list(tSet)
    for t in tSet:
        neigh.extend(list(g.neighbors(t)))
    Set=set(neigh)
    for t in Set:
        neigh.extend(list(g.neighbors(t)))

    neigh=set(neigh).difference(tSet)

    C=nx.betweenness_centrality(g, k=100)
    seed=set(sorted(C, key=lambda x: C[x] if (x in neigh) else 0, reverse=True)[0:seedsize])
    return seed

def neighs(g,p, seedsize, tSet=None, r=1):
    seed=set()
    neigh=set()
    D=dict(g.degree)
    ss=10

    while len(seed)<seedsize:
        ss=min(10, seedsize-len(seed))
        s=max(D, key=lambda x:D[x])
        seed=seed.union(sampling.snow(g, seed=s, maxsize=ss))
        del D[s]
        seed=seed.difference(tSet)
    return seed

def neisinD(g,p, seedsize, tSet=None, r=1):
    l=dict(g.degree)
    L=copy.deepcopy(l)
    seed=set()
    avgd=g.size()/g.number_of_nodes()
    neigh=set()
    for t in tSet:
        neigh=neigh.union(set(g.neighbors(t)))
    while True:
        v=max(l, key=lambda x:l[x])
        if not v in tSet:
            seed.add(v)
        nei=set(g.neighbors(v))
        d=dict((k,L[k]) for k in nei)
        for i in range(0,min(len(nei),5)):
            v1=max(d, key=lambda x:d[x])
            if v1 in neigh and d[v1]>avgd:
                seed.add(v1)
            if d[v1]<2*avgd or len(seed)>=seedsize:
                break
            if not (v1 in tSet):
                seed.add(v1)

        if len(seed)>=seedsize:
            break
        del l[v]
    return seed
