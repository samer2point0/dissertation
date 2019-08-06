import networkx as nx
import random
import copy
import queue
import sampling
import tools
import pres

def randseed(g, p, seedsize, tSet=None, r=1):
    nodes=list(g.nodes)
    seed= set(random.choices(nodes,k=seedsize))
    while len(seed)<seedsize:
        seed.add(random.choice(nodes))
    return seed

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
    for i in range(0,4):
        nei=set()
        for t in Set[i]:
            nei=nei.union(set(g.neighbors(t)))
        nei=nei.difference(neigh)
        Set.append(nei)
        neigh=neigh.union(nei)

    neigh=neigh.difference(tSet)

    for i in range(1,5):
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

def voterank(g,p, seedsize, tSet=None, r=1):
    C=nx.voterank(g, number_of_nodes=seedsize)
    return set(C)

def voteN(g,p, seedsize, tSet=None, r=1):
    t=5
    Q=copy.deepcopy(tSet)
    V={}
    D=dict(g.degree)
    for i in range(0,t):
        q=copy.deepcopy(Q)
        for x in q:
            if not x in V:
                V[x]=0
            V[x]=V[x]-1
            Q.remove(x)

            vote=max(g.neighbors(x), key=lambda x:D[x] if not x in tSet else 0)
            if not vote in V:
                V[vote]=0
            V[vote]=V[vote]+1
            Q.add(vote)

        Q=Q.union(tSet)

    seed=set(sorted(V, key=lambda x: V[x], reverse=True)[0:seedsize])
    return seed

def close(g,p, seedsize, tSet=None, r=1):
    l=sorted(g.degree, key=lambda x: x[1], reverse=True)
    tpot=[x[0] for x in l if x not in tSet][0:int(seedsize*2)]
    pot=set(tpot)
    CD={}
    flag=set()
    sw=10

    for t in tSet:
        Set=set(g.neighbors(t))
        for n in Set:
            if ((n in pot) and (not (t,n) in flag)):
                flag.add((t,n))
                if not n in CD:
                    CD[n]=0
                CD[n]=CD[n]+1

            Set1=set([x for x in g.neighbors(n) if x not in Set])
            for n1 in Set1:
                if ((n1 in pot) and (not (t,n1) in flag)):
                    flag.add((t,n1))
                    if not n1 in CD:
                        CD[n1]=0
                    CD[n1]=CD[n1]+2

                Set2=set([x for x in g.neighbors(n1) if x not in (Set.union(Set1))])
                for n2 in Set2:
                    if ((n2 in pot) and (not (t,n2) in flag)):
                        flag.add((t,n2))
                        if not n2 in CD:
                            CD[n2]=0
                        CD[n2]=CD[n2]+3


        leftpot=[x for x in pot if not (t,x) in flag]
        for p in leftpot:
            flag.add((t,p))
            if not p in CD:
                CD[p]=0
            CD[p]=CD[p]+sw

    seed=set(sorted(CD, key=lambda x: CD[x], reverse=False)[0:seedsize])
    print(len(seed.intersection(set(tpot[0:seedsize]))))

    return seed
