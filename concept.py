import networkx as nx
import matplotlib.pyplot as plt
import random
import queue

def randseed(g, size):
    return random.choices(g.nodes,k=size)

class Concept():
    def __init__(self,g,name,seedsize=10,func=randseed,factor=0.9):
        self.factor=factor
        self.seed=func(g,seedsize)
        self.newNodes=seed
        self.name=name
        for node in seed:
            g.nodes[node][name]=True

    def update(self):
        #loops over all the recently activated nodes, rather than interwining concept activation
        newN=[]
        while self.newNodes:
            node=self.newNodes.pop()
            neigh=g.neighbors(node)
            for n in neigh:
                p=random.random()
                if p < self.factor/len(neigh): #NONWEIGHTED GRAPH
                    if g.nodes[n][self.name]==False:
                        g.nodes[n][self.name]=True
                        newN.append(n)
        self.newNodes=newN
