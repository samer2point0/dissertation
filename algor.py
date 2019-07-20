import networkx as nx
import random
import algor

def randseed(g, p, seedsize):
    return set(random.choices(list(g.nodes),k=seedsize))

def degree(g, seedsize=100):
    l=sorted(g.degree, key=lambda x: x[1], reverse=True)
    return set([x[0] for x in l[0:seedsize]])


def sinDisc(g,p,  seedsize):
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


def degDisc(g,p, seedsize):
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

        tv=len(set(g.neighbors(seed[0])).union(set(seed)))
        x=(x[0],x[1]-2*tv-(x[1]-tv)*p) #discount 1 for each edge alfeady in set
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
