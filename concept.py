import networkx as nx
import matplotlib.pyplot as plt
import random
import queue
import copy

concepts=set(['target', 'pro', 'anti'])

def randseed(g, size):
    return set(random.choices(list(g.nodes),k=size))

class Concept():
    def __init__(self,g,name,seedsize=100,func=randseed,PP=0.08, r=[2,0.5]):
        self.PP=PP
        self.name=name
        self.g=g
        #set up multicpncept influence factors for pr ant case
        self.r=dict(zip(concepts,[1,1,1]))#influence for reciever and sender is the same
        if name=='target':
            self.r['B']=r[0]
            self.r['inH']=r[1]
        #set up seed sets
        self.seed=func(g,seedsize)
        self.newNodes=self.seed
        self.active=copy.deepcopy(self.newNodes)
        for node in self.seed:
            g.nodes[node]['concept']=set(name)


    def update(self):
        #loops over all the recently activated nodes, rather than interwining concept activation
        newN=set()
        while self.newNodes:
            node=self.newNodes.pop()
            neigh=self.g.neighbors(node)
            for n in neigh:
                p=random.random()
                CI=self.context(node,n)#NONWEIGHTED GRAPH
                if p < CI:
                    if not n in self.active:
                        try:
                            self.g.nodes[n]['concept'].add(self.name)
                        except (KeyError, TypeError) as e:
                            self.g.nodes[n]['concept']=set([self.name])
                        self.active.add(n)
                        newN.add(n)
        self.newNodes=newN

    def context(self, send, rec):
        ci=self.PP
        try:
            for c in send['concept']:
                ci=ci*self.r[c]
        except (KeyError, TypeError) as e:
            pass
        try:
            for c in rec['concept']:
                ci=ci*self.r[c]
        except (KeyError, TypeError) as e:
            pass

        ci=min(1,ci)
        return ci
