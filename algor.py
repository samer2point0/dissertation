import networkx as nx
import random
import copy


def randseed(g, p, seedsize, tSet=None, r=1):
    return set(random.choices(list(g.nodes),k=seedsize))

def degree(g,p, seedsize, tSet=None, r=1):
    l=sorted(g.degree, key=lambda x: x[1], reverse=True)
    return set([x[0] for x in l[0:seedsize]])


def sinDisc(g,p,  seedsize, tSet=None, r=1):
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


def degDisc(g,p, seedsize, tSet=None, r=1):
    l=sorted(g.degree, key=lambda x: x[1])
    seed=[l.pop()[0]]
    neigh=list(g.neighbors(seed[0]))
    pot=[l.pop()]
    if pot in neigh:
        pot[0][1]=pot[0][1]-1

    while True:
        if l ==[]:
            seed.extend(list(zip(*pot))[0])
            break
        x=l.pop()
        while (not pot==[]) and x[1]<pot[-1][1]:
            seed.insert(0, pot.pop()[0])
            neigh.extend(list(g.neighbors(seed[0])))

        if len(seed)>=seedsize:
            break

        tv=len(set(g.neighbors(seed[0])).intersection(set(seed)))
        x=(x[0],x[1]-2*tv-(x[1]-tv)*p*tv) #discount 1 for each edge alfeady in set
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

def MPG(g,p, seedsize, tSet=None, r=1):
    thresh=0.001
    N=dict()
    seed=set()
    neigh=set()
    i=1
    Set=tSet
    if Set==None:
        print('WHAAAAAT')
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


    R=copy.deepcopy(N)
    while True:
        v=max(R, key=lambda x:R[x]['we'])
        seed.add(v)
        if len(seed)==seedsize:
            break

        #update expected gain
        for pa in N[v]['parents']:
            N[pa]['eg']=N[pa]['eg']-p+r*p
            N[pa]['we']=N[pa]['ap']*N[pa]['eg']

        #update activation prob
        nei=neigh.intersection(g.neighbors(v))
        for k in nei:
            N[k]['ap']=N[k]['ap']-p+p*r
            N[k]['we']=N[k]['ap']*N[k]['eg']

        del R[v]

    return seed

def bet(g,p, seedsize, tSet=None, r=1):
    pass
