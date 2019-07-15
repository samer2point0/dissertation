import networkx as nx
import matplotlib.pyplot as plt
import random
import queue

concepts=set(['target', 'pro', 'anti'])

def randseed(g, size):
    return set(random.choices(list(g.nodes),k=size))

class Concept():
    def __init__(self,g,name,seedsize=10,func=randseed,factor=0.1):
        self.factor=factor
        self.name=name
        self.g=g
        #set up multicpncept influence factors for pr ant case
        self.r=dict(zip(concepts,[1,1,1]))#influence for reciever and sender is the same
        if name=='target':
            self.r['pro']=1.1
            self.r['anti']=0.9
        #set up seed sets
        self.seed=func(g,seedsize)
        self.newNodes=self.seed
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
                    try: #concepts activate once
                        if not self.name in self.g.nodes[n]['concept']:
                            self.g.nodes[n]['concept'].add(self.name)
                            newN.add(n)
                    except (KeyError, TypeError) as e:
                        self.g.nodes[n]['concept']=set(self.name)
                        newN.add(n)
        self.newNodes=newN

    def context(self, send, rec):
        ci=self.factor
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
