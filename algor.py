import networkx as nx
import random
import algor

def randseed(g, seedsize=100):
    return set(random.choices(list(g.nodes),k=seedsize))

def degree(g, seedsize=100):
    l=sorted(g.degree, key=lambda x: x[1], reverse=True)
    return set([x[0] for x in l[0:seedsize]])

def degDisc(g, seedsize=100):
    pass
