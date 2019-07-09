import networkx as nx
import matplotlib.pyplot as plt
import random
import queue

concepts=set('target', 'pro', 'anti')

def randseed(g, size):
    return random.choices(g.nodes,k=size)

class Concept():
    def __init__(self,g,name,seedsize=10,func=randseed,factor=0.9):
        self.factor=factor
        self.name=name
        #set up multicpncept influence factors for pr ant case
        self.r=zip(concepts,[1,1,1])#influence for reciever and sender is the same
        if name='target':
            self.r['pro']=1.1
            self.r['anti']=0.9
        #set up seed sets
        self.seed=func(g,seedsize)
        self.newNodes=seed
        for node in seed:
            g.nodes[node]['concept']=set(name)


    def update(self):
        #loops over all the recently activated nodes, rather than interwining concept activation
        newN=[]
        while self.newNodes:
            node=self.newNodes.pop()
            neigh=g.neighbors(node)
            for n in neigh:
                p=random.random()
                CI=self.context(node,n)#NONWEIGHTED GRAPH
                if p < CI:
                    try: #concepts activate once
                        if not self.name in g.nodes[n]['concept']:
                            g.nodes[n]['concept'].add(self.name)
                            newN.append(n)
                    except KeyError:
                        g.nodes[n]['concept']=set(self.name)
                        newN.append(n)
        self.newNodes=newN

    def context(send, rec):
        ci=self.factor
        try:
            for c in send['concept']:
                ci=ci*self.r[c]
        except KeyError:
            pass
        try:
            for c in rec['concept']:
                ci=ci*self.r[c]
        except KeyError:
            pass

        ci=min(1,ci)
        return ci
